"""
github_trending.py — 爬取 GitHub Trending 页面。

目标页面: https://github.com/trending
提取当日热门仓库的名称、描述、语言、Star 数和今日新增。
"""

from __future__ import annotations

import datetime as dt
import re

import httpx
from bs4 import BeautifulSoup

NAME = "GitHub Trending"
SLUG = "github-trending"
CATEGORY = "community"

_URL = "https://github.com/trending"
_HEADERS = {"User-Agent": "Mozilla/5.0 learn-ai-bot"}


def scrape(since: dt.datetime | None = None) -> list[dict]:
    """爬取 GitHub Trending，返回条目列表。

    Args:
        since: 此爬虫忽略该参数（Trending 页面本身就是当天数据）。
    """
    resp = httpx.get(_URL, follow_redirects=True, timeout=30, headers=_HEADERS,
                     verify=False)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    entries: list[dict] = []
    today = dt.date.today().isoformat()

    for article in soup.select("article.Box-row"):
        # 仓库名: h2 > a
        h2 = article.select_one("h2 a")
        if not h2:
            continue
        repo_path = h2.get("href", "").strip("/")
        if not repo_path:
            continue
        repo_name = repo_path  # e.g. "owner/repo"

        # 描述
        desc_tag = article.select_one("p")
        description = desc_tag.get_text(strip=True) if desc_tag else ""

        # 语言
        lang_tag = article.select_one("[itemprop='programmingLanguage']")
        language = lang_tag.get_text(strip=True) if lang_tag else ""

        # 总 Star 数
        star_links = article.select("a.Link--muted")
        total_stars = ""
        forks = ""
        if len(star_links) >= 1:
            total_stars = star_links[0].get_text(strip=True).replace(",", "")
        if len(star_links) >= 2:
            forks = star_links[1].get_text(strip=True).replace(",", "")

        # 今日 Star
        today_stars_tag = article.select_one("span.d-inline-block.float-sm-right")
        today_stars = ""
        if today_stars_tag:
            today_stars = today_stars_tag.get_text(strip=True)

        # 组装摘要
        parts = []
        if language:
            parts.append(language)
        if total_stars:
            parts.append(f"Stars: {total_stars}")
        if forks:
            parts.append(f"Forks: {forks}")
        if today_stars:
            parts.append(today_stars)
        summary = " | ".join(parts)

        link = f"https://github.com/{repo_path}"

        entries.append({
            "title": repo_name,
            "link": link,
            "summary": summary,
            "published": today,
            "source": NAME,
            "slug": SLUG,
            "cat": CATEGORY,
        })

    return entries
