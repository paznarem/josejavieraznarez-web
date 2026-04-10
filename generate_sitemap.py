#!/usr/bin/env python3
"""
Generate sitemap.xml for josejavieraznarez.com

Scans all published HTML files, excludes drafts and templates,
and supports multi-language pages via hreflang alternates.

Usage:
    python generate_sitemap.py
"""

import pathlib
import re
from datetime import date
from xml.etree import ElementTree as ET

# ── Config ────────────────────────────────────────────────────────────────────

BASE_URL = "https://www.josejavieraznarez.com"
ROOT = pathlib.Path(__file__).parent

# Files/dirs to exclude from the sitemap
EXCLUDE_PATTERNS = [
    "articulos sin publicar*",          # draft articles
    "serie toca aunque tiembles/*",     # source files (not the blog output)
    "blog-template.html",
    "consentimiento-tarifas.html",
    "aviso-legal.html",                 # low-value legal pages (optional: remove to include)
    "autocompasion-autoestima-genuina.html",  # duplicate of blog/ version (root draft)
]

# Directories that contain published content
INCLUDE_DIRS = [
    ROOT,           # root HTML files (index, sobre-mi, etc.)
    ROOT / "blog",
]

# Priority and changefreq by path pattern (first match wins)
PRIORITY_RULES = [
    (r"^/$",              "1.0", "weekly"),
    (r"^/blog/$",         "0.9", "weekly"),
    (r"^/blog/",          "0.8", "monthly"),
    (r".*",               "0.6", "monthly"),
]

# ── Multi-language support ────────────────────────────────────────────────────
# When you add pages in another language, map them here.
# Format: { "/path/es/page.html": "/path/en/page.html", ... }
# The sitemap will add <xhtml:link rel="alternate" hreflang="..."> entries.
#
# Example:
#   LANGUAGE_ALTERNATES = {
#       "/sobre-mi.html": {
#           "es": "/sobre-mi.html",
#           "en": "/en/about-me.html",
#       },
#   }
LANGUAGE_ALTERNATES: dict[str, dict[str, str]] = {}

# Default language for pages not listed in LANGUAGE_ALTERNATES
DEFAULT_LANG = "es"

# ── Helpers ───────────────────────────────────────────────────────────────────

def is_excluded(path: pathlib.Path) -> bool:
    rel = path.relative_to(ROOT)
    for pattern in EXCLUDE_PATTERNS:
        if rel.match(pattern):
            return True
    return False


def collect_html_files() -> list[pathlib.Path]:
    files = []
    for directory in INCLUDE_DIRS:
        for html in sorted(directory.glob("*.html")):
            if not is_excluded(html):
                files.append(html)
    return files


def path_to_url(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT)
    url_path = "/" + rel.as_posix()
    # Shorten index.html → directory URL
    if url_path.endswith("/index.html"):
        url_path = url_path[: -len("index.html")]
    return BASE_URL + url_path


def get_priority_and_freq(url: str) -> tuple[str, str]:
    path = url.replace(BASE_URL, "")
    for pattern, priority, freq in PRIORITY_RULES:
        if re.match(pattern, path):
            return priority, freq
    return "0.5", "monthly"


def get_lastmod(path: pathlib.Path) -> str:
    """Use git last-commit date if available, else today."""
    try:
        import subprocess
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", str(path)],
            capture_output=True, text=True, cwd=ROOT
        )
        date_str = result.stdout.strip()
        if date_str:
            return date_str
    except Exception:
        pass
    return date.today().isoformat()


# ── Sitemap builder ───────────────────────────────────────────────────────────

SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
XHTML_NS = "http://www.w3.org/1999/xhtml"

ET.register_namespace("", SITEMAP_NS)
ET.register_namespace("xhtml", XHTML_NS)


def build_sitemap(files: list[pathlib.Path]) -> ET.Element:
    urlset = ET.Element(
        "urlset",
        {
            "xmlns": SITEMAP_NS,
            "xmlns:xhtml": XHTML_NS,
        },
    )

    for path in files:
        url_str = path_to_url(path)
        priority, freq = get_priority_and_freq(url_str)
        lastmod = get_lastmod(path)

        rel_path = "/" + path.relative_to(ROOT).as_posix()

        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = url_str
        ET.SubElement(url_el, "lastmod").text = lastmod
        ET.SubElement(url_el, "changefreq").text = freq
        ET.SubElement(url_el, "priority").text = priority

        # hreflang alternates (multi-language support)
        alternates = LANGUAGE_ALTERNATES.get(rel_path)
        if alternates:
            for lang, lang_path in alternates.items():
                ET.SubElement(
                    url_el,
                    "{http://www.w3.org/1999/xhtml}link",
                    {
                        "rel": "alternate",
                        "hreflang": lang,
                        "href": BASE_URL + lang_path,
                    },
                )
        else:
            # Single-language page: self-referential hreflang
            ET.SubElement(
                url_el,
                "{http://www.w3.org/1999/xhtml}link",
                {
                    "rel": "alternate",
                    "hreflang": DEFAULT_LANG,
                    "href": url_str,
                },
            )

    return urlset


def indent(elem: ET.Element, level: int = 0) -> None:
    """Pretty-print helper (Python < 3.9 compatible)."""
    indent_str = "\n" + "  " * level
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = indent_str + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = indent_str
        for child in elem:
            indent(child, level + 1)
        if not child.tail or not child.tail.strip():
            child.tail = indent_str
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = indent_str


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    files = collect_html_files()
    print(f"Found {len(files)} HTML files to index:")
    for f in files:
        print(f"  {f.relative_to(ROOT)}")

    urlset = build_sitemap(files)
    indent(urlset)

    tree = ET.ElementTree(urlset)
    out_path = ROOT / "sitemap.xml"
    tree.write(out_path, encoding="UTF-8", xml_declaration=True)

    print(f"\nSitemap written to {out_path}")
    print(f"  {len(files)} URLs included")
    print(f"  Date: {date.today().isoformat()}")


if __name__ == "__main__":
    main()
