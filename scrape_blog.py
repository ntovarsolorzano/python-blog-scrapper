#!/usr/bin/env python3
"""
scrape_blog.py

Fetches a single blog-post URL, extracts title, date, and the main body
text, converts the body to Markdown, and writes:

    workspace/scrapped websites/<sanitized-title>.md

Usage:
    python scrape_blog.py https://example.com/blog-post
"""

import os
import re
import sys
import unicodedata
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from dateutil import parser as date_parser
from markdownify import markdownify

# ------------------------------------------------------------------ helpers
USER_AGENT = ("Mozilla/5.0 (compatible; BlogScraper/1.0; "
              "+https://github.com/yourname/blog-scraper)")

HEADERS = {"User-Agent": USER_AGENT}

def slugify(value: str) -> str:
    """Turn a string into a filesystem-safe name."""
    value = unicodedata.normalize("NFKD", value)
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[-\s]+", "-", value)

def fetch_html(url: str) -> str:
    """Download raw HTML."""
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text

def extract_common(soup: BeautifulSoup) -> tuple[str, str | None]:
    """Try to find title and publication date with common patterns."""
    # --- title ---------------------------------------------------------
    title = ""
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
    # OpenGraph fallback
    og_title = soup.find("meta", property="og:title")
    if og_title and og_title.get("content"):
        title = og_title["content"].strip()

    # --- date ----------------------------------------------------------
    date = None
    # 1. <time datetime="...">
    time_tag = soup.find("time")
    if time_tag and time_tag.has_attr("datetime"):
        try:
            date = str(date_parser.parse(time_tag["datetime"]).date())
        except Exception:
            pass
    # 2. JSON-LD
    if not date:
        ld = soup.find("script", type="application/ld+json")
        if ld:
            try:
                import json
                data = json.loads(ld.string)
                if isinstance(data, dict):
                    dt = data.get("datePublished") or data.get("dateCreated")
                    if dt:
                        date = str(date_parser.parse(dt).date())
            except Exception:
                pass
    # 3. meta[name="article:published_time"]
    if not date:
        meta_pub = soup.find("meta", attrs={"name": "article:published_time"})
        if meta_pub:
            try:
                date = str(date_parser.parse(meta_pub["content"]).date())
            except Exception:
                pass
    return title, date

def detect_main_content(soup: BeautifulSoup) -> str:
    """
    Very small heuristic to find the 'main' article container.
    Priority: <article>, role="main", <main>, .post, .entry-content, …
    Falls back to entire <body>.
    """
    selectors = [
        "article",
        "main",
        "[role='main']",
        ".post",
        ".entry-content",
        ".post-content",
        ".article-body",
        "#content",
    ]
    for sel in selectors:
        container = soup.select_one(sel)
        if container:
            return str(container)
    return str(soup.body)  # last resort

def clean_html(html: str) -> str:
    """Remove script/style tags and obvious clutter."""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()
    return str(soup)

def html_to_markdown(html: str) -> str:
    """Convert cleaned HTML to Markdown."""
    return markdownify(html, heading_style="ATX", strip=["a"])

# ------------------------------------------------------------------ main
def process_url(url: str) -> None:
    html = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    title, date = extract_common(soup)

    main_html = detect_main_content(soup)
    cleaned = clean_html(main_html)
    md_body = html_to_markdown(cleaned).strip()

    # Build final markdown
    lines = [f"# {title}"]
    if date:
        lines.append(f"\n*Published on {date}*\n")
    lines.append("\n")
    lines.append(md_body)
    lines.append(f"\n\n---\nTaken from: {url}")

    # Save to file
    output_dir = Path("workspace/scrapped websites")
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = slugify(title) + ".md"
    output_path = output_dir / filename
    output_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Saved to {output_path.resolve()}")

# ------------------------------------------------------------------ CLI
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape_blog.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    # Basic URL sanity
    parsed = urlparse(url)
    if not parsed.scheme:
        print("Please provide a full URL including http/https.")
        sys.exit(1)
    try:
        process_url(url)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)