README.md
==========

> 🚀 **One-liner pitch:** paste any blog-post URL → get a clean Markdown file in `workspace/scrapped websites/`.

---

## 🔧 Installation (local)

```bash
git clone <this-repo>
cd <this-repo>

python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### 📦 requirements.txt
```text
requests>=2.31.0
beautifulsoup4>=4.12.2
markdownify>=0.12.1
python-dateutil>=2.8.2
```

---

## ▶️ Usage

### Option A – Local CLI
```bash
python scrape_blog.py https://example.com/interesting-article
```

### Option B – **Zero-install Colab notebook**  
Open the ready-to-run Google Colab 🪄  
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1dsqibQa21-IV2KL1X9Opmwi1qL7aRkoC?usp=sharing)

> Paste any URL in the first cell, execute, and download the `.md` straight from the notebook!

---

## 📁 Output structure

```
workspace/
└── scrapped websites/
    └── how-to-train-your-dragon.md   # sanitized title
```

Each file looks like:

```markdown
# How to Train Your Dragon
*Published on 2024-07-26*

Once upon a time …

---

Taken from: https://example.com/interesting-article
```

---

## 🛠️ Customisation

| What to tweak | Where to look |
|---------------|---------------|
| CSS selectors for main content | `detect_main_content()` |
| Extra date sources | `extract_common()` |
| Auth / JS rendering | replace `requests` with `playwright` or `selenium` |

---

## ❓ Troubleshooting

* **SSL errors** → upgrade certificates or add `verify=False`
* **Wrong date format** → extend `dateutil.parser` rules
* **File-name collisions** → append a timestamp in `slugify()`

---

## 📄 License

MIT – feel free to fork, tweak, and share!