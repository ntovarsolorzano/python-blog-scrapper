README.md
==========

A tiny, self-contained Python “agent” that turns any blog-post URL into a clean, single Markdown file.

Installation
------------

```bash
git clone <this-repo>
cd <this-repo>

# Create a virtual env (optional but recommended)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt   # or manually:
# pip install requests beautifulsoup4 markdownify python-dateutil
```

Usage
-----

```bash
python scrape_blog.py https://example.com/interesting-article
```

The script downloads the page, extracts:

* Title  
* Publication date (if found)  
* Body text (ignoring nav, footer, ads, etc.)  

…and writes a file to

```
workspace/scrapped websites/<sanitized-title>.md
```

Example output
--------------

```
# How to Train Your Dragon
*Published on 2024-07-26*

Once upon a time …

---

Taken from: https://example.com/interesting-article
```

Folder structure
----------------

```
.
├── scrape_blog.py          # main script
├── requirements.txt        # pip dependencies
└── workspace/scrapped websites/   # output directory (auto-created)
```

Customisation
-------------

1. **Tweak content extraction**  
   Edit the CSS selector list inside `detect_main_content()` in `scrape_blog.py`.

2. **Add new date sources**  
   Extend `extract_common()` if your target site uses custom markup.

3. **Authentication / JS rendering**  
   Replace the `requests` call with `playwright` or `selenium` if pages are behind login walls or rendered client-side.

Troubleshooting
---------------

* **SSL / certificate errors**: upgrade certificates or pass `verify=False` to `requests.get`.  
* **Wrong date format**: ensure the site’s date string is parseable by `dateutil.parser`.  
* **File name collisions**: the script sanitizes titles, but you can add a timestamp suffix if desired.

License
-------

MIT – do whatever you like.