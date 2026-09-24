#!/usr/bin/env python3
"""Save ScaleDojo's free Learn chapters (allowed by its robots.txt) as Markdown for Faiz's personal study.

Output goes to private/scaledojo/learn/<track>/<module>/<chapter>.md, which git ignores: the content is
ScaleDojo's and must not be published. One request every 1.5 s; pages already saved are skipped.

    python3 scripts/scrape_scaledojo_learn.py            # all five courses
    python3 scripts/scrape_scaledojo_learn.py genai      # one course
"""
import html
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "private" / "scaledojo" / "learn"
UA = {"User-Agent": "Mozilla/5.0 (personal study copy; FaizOS)"}


def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40).read().decode("utf-8", "ignore")


class Main(HTMLParser):
    """Turn the <main> element into Markdown: headings, paragraphs, lists, code, tables; skip scripts and buttons."""
    BLOCK = {"p": "\n\n", "li": "\n- ", "tr": "\n", "br": "\n"}

    def __init__(self):
        super().__init__()
        self.depth, self.skip, self.out, self.pre = 0, 0, [], 0

    def handle_starttag(self, tag, attrs):
        if tag == "main":
            self.depth += 1
        if not self.depth:
            return
        if tag in ("script", "style", "button", "svg", "nav"):
            self.skip += 1
        elif tag in ("h1", "h2", "h3", "h4"):
            self.out.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "pre":
            self.pre += 1
            self.out.append("\n\n```\n")
        elif tag in ("td", "th"):
            self.out.append(" | ")
        elif tag in self.BLOCK:
            self.out.append(self.BLOCK[tag])

    def handle_endtag(self, tag):
        if tag == "main":
            self.depth -= 1
        if not self.depth:
            return
        if tag in ("script", "style", "button", "svg", "nav"):
            self.skip -= 1
        elif tag == "pre":
            self.pre -= 1
            self.out.append("\n```\n")

    def handle_data(self, data):
        if self.depth and not self.skip:
            self.out.append(data if self.pre else re.sub(r"\s+", " ", data))

    def markdown(self):
        text = html.unescape("".join(self.out))
        text = re.sub(r"[ \t]+\n", "\n", text)
        return re.sub(r"\n{3,}", "\n\n", text).strip() + "\n"


def main(tracks):
    sitemap = get("https://scaledojo.dev/sitemap.xml")
    urls = [u for u in re.findall(r"<loc>([^<]+)</loc>", sitemap) if "/learn/" in u]
    urls = [u for u in urls if u.split("/")[3] in tracks] if tracks else urls
    done = failed = 0
    for url in urls:
        parts = url.rstrip("/").split("/")          # https: '' scaledojo.dev <track> learn <module> <chapter>
        if len(parts) < 7:
            continue
        out = ROOT / parts[3] / parts[5] / f"{parts[6]}.md"
        if out.exists():
            continue
        try:
            page = Main()
            page.feed(get(url))
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(f"<!-- source: {url} -->\n\n" + page.markdown())
            done += 1
        except Exception as e:                       # keep going; report at the end
            failed += 1
            print(f"FAILED {url}: {e}", file=sys.stderr)
        time.sleep(1.5)
    print(f"saved {done}, failed {failed}, of {len(urls)} chapter URLs")


if __name__ == "__main__":
    main(sys.argv[1:])
