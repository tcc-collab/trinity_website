"""
Scrapers Package

This package contains following modules:
 notice:
 events:
 login:
 navigation:
 news:

__vars__:
TRINITY_LINK -> [str] URL of Trinity college, Dilibazar, Kathmandu

__Functions__:
get_html -> <requests.HTML> object
"""
import os
from pathlib import Path

from requests_html import HTML, HTMLSession

CACHE_DIR = Path.home() / "cache/trinity_cache"
TRINITY_LINK = "http://trinitycollege.edu.np/"


def get_html(url=TRINITY_LINK, cache=True, rendered=False):
    """
    Returns a valid <requests HTML> object.
    Params:
        url: [str] URL of page. Default trinity homepage
    """
    html = None

    print("CACHE", cache)
    if cache:
        html = __get_html_from_cache(url)
    if not html:
        print("FETCHING", url)
        html = fetch_html(url, rendered=rendered)
    return html


def __get_html_from_cache(url):
    """
    Loads <requests HTML> object from cache files
    Params:
        url = [str] URL of page to load
    """
    event_url = "http://trinitycollege.edu.np/trinity.php?cal=calen"
    news_url = "http://trinitycollege.edu.np/?page=news&type=news"
    notice_url = "http://trinitycollege.edu.np/?page=news&type=notice"

    link_resource_map = {
        TRINITY_LINK: "index.html",
        event_url: "all_events.html",
        news_url: "all_news.html",
        notice_url: "all_notice.html",
    }

    try:
        index_file = CACHE_DIR / link_resource_map[url]
        if not index_file.exists():
            os.makedirs(str(index_file.parent))
        with open(index_file, "r", encoding="utf-8") as rf:
            html_str = rf.read()
        html_soup = HTML(html=html_str, url=url)
        print(f"{url} Loaded from cache {index_file}")
        return html_soup
    except Exception as E:
        print(E)
        return None


def fetch_html(url, rendered=False):
    """
    Fetch html from web.
    Returns -> <requests HTML> object.
    Params -> URL of the web resource.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/39.0.2171.95 Safari/537.36"
        )
    }

    session = HTMLSession()
    result = session.get(url, headers=headers)
    if rendered:
        result.html.render()
    return result.html
