# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "feedparser>=6.0",
# ]
# ///
"""
daily_update.py — 拉取 AI 社区 RSS，写入 journal 原始素材。

用法:
    uv run scripts/daily_update.py            # 拉取过去 24h
    uv run scripts/daily_update.py --hours 48 # 拉取过去 48h

输出:
    journal/YYYY/MM/DD.md  — 当日原始条目，按来源分类
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import io
import os
import re
import sys
import textwrap
from pathlib import Path

# Windows 控制台默认编码不支持中文，强制使用 UTF-8
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import feedparser

# ──────────────────────────────────────────────
# RSS 源（经过验证可用的）
# ──────────────────────────────────────────────
RSS_FEEDS: list[dict] = [
    # 论文
    {"name": "arXiv cs.AI", "url": "https://rss.arxiv.org/rss/cs.AI", "cat": "papers"},
    {"name": "arXiv cs.CL", "url": "https://rss.arxiv.org/rss/cs.CL", "cat": "papers"},
    # 厂商博客
    {"name": "OpenAI", "url": "https://openai.com/blog/rss.xml", "cat": "industry"},
    {"name": "DeepMind", "url": "https://deepmind.google/blog/rss.xml", "cat": "industry"},
    # 社区 / 独立博主
    {"name": "Latent Space", "url": "https://www.latent.space/feed", "cat": "community"},
    {"name": "Sebastian Raschka", "url": "https://magazine.sebastianraschka.com/feed", "cat": "community"},
    {"name": "Simon Willison", "url": "https://simonwillison.net/atom/everything/", "cat": "community"},
]

REPO_ROOT = Path(__file__).resolve().parent.parent
JOURNAL_DIR = REPO_ROOT / "journal"

TODAY = dt.date.today()

TAG_RE = re.compile(r"<[^>]+>")


def strip_html(text: str) -> str:
    """去除 HTML 标签，反转义。"""
    return html.unescape(TAG_RE.sub("", text)).strip()


# ──────────────────────────────────────────────
# 拉取
# ──────────────────────────────────────────────
def fetch_feed(cfg: dict, since: dt.datetime) -> list[dict]:
    entries: list[dict] = []
    try:
        parsed = feedparser.parse(cfg["url"])
        for e in parsed.entries[:30]:
            pub = None
            for attr in ("published_parsed", "updated_parsed"):
                ts = getattr(e, attr, None)
                if ts:
                    pub = dt.datetime(*ts[:6])
                    break
            if pub and pub < since:
                continue
            summary = strip_html(getattr(e, "summary", ""))[:200]
            entries.append({
                "title": getattr(e, "title", "Untitled").strip(),
                "link": getattr(e, "link", ""),
                "summary": summary,
                "source": cfg["name"],
                "cat": cfg["cat"],
            })
    except Exception as exc:
        print(f"  [WARN] {cfg['name']}: {exc}")
    return entries


def fetch_all(since: dt.datetime) -> list[dict]:
    all_entries: list[dict] = []
    for cfg in RSS_FEEDS:
        print(f"  {cfg['name']} ...", end=" ", flush=True)
        items = fetch_feed(cfg, since)
        all_entries.extend(items)
        print(f"{len(items)} 条")
    return all_entries


# ──────────────────────────────────────────────
# 格式化
# ──────────────────────────────────────────────
CAT_LABELS = {
    "papers": "论文",
    "industry": "厂商动态",
    "community": "社区",
}


def format_entries(entries: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = {}
    for e in entries:
        by_cat.setdefault(e["cat"], []).append(e)

    sections: list[str] = []
    for cat_key, label in CAT_LABELS.items():
        items = by_cat.get(cat_key, [])
        sec = f"## {label}\n\n"
        if not items:
            sec += "(无)\n"
        else:
            for e in items:
                line = f"- [{e['source']}] **{e['title']}**"
                if e["summary"]:
                    line += f" — {e['summary']}"
                if e["link"]:
                    line += f"  \n  {e['link']}"
                sec += line + "\n"
        sections.append(sec)
    return "\n".join(sections)


# ──────────────────────────────────────────────
# 写入
# ──────────────────────────────────────────────
def write_journal(date: dt.date, body: str) -> Path:
    p = JOURNAL_DIR / str(date.year) / f"{date.month:02d}" / f"{date.day:02d}.md"
    p.parent.mkdir(parents=True, exist_ok=True)

    content = textwrap.dedent(f"""\
        ---
        date: {date.isoformat()}
        type: daily
        ---

        # {date.isoformat()} AI 动态

    """)
    content += body + "\n"
    p.write_text(content, encoding="utf-8")
    return p


# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="拉取 AI RSS 写入 journal")
    ap.add_argument("--hours", type=int, default=24, help="回溯小时数 (默认 24)")
    args = ap.parse_args()

    since = dt.datetime.now() - dt.timedelta(hours=args.hours)
    print(f"[{TODAY}] 拉取过去 {args.hours}h ...\n")

    entries = fetch_all(since)
    total = len(entries)
    print(f"\n共 {total} 条\n")

    if not entries:
        print("无新条目。")
        return

    body = format_entries(entries)
    p = write_journal(TODAY, body)
    print(f"=> {p}")


if __name__ == "__main__":
    main()
