"""
News package:
get_top_news -> [List] list of recent news[type dict]
news_page_link -> [str] link of news page containing all notices
get_all_news -> [List] list of all news[type dict]
"""

from backend.scrapers.news.main import get_all_news, get_top_news, news_page_link
