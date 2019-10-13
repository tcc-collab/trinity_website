from flask import Flask, render_template

from backend.scrapers import get_html
from backend.scrapers.downloadable import get_downloadable
from backend.scrapers.events import event_page_link, get_top_event
from backend.scrapers.footer import get_footer
from backend.scrapers.news import get_all_news, get_top_news, news_page_link
from backend.scrapers.notice import get_all_notice, get_top_notice, notice_page_link
from backend.utils import get_navbar


app = Flask(__name__)


@app.route("/")
def home():
    html = get_html(cache=True)
    top_notice = get_top_notice(html)
    top_events = get_top_event(html)
    top_news = get_top_news(html)
    main_navs, nested_navs = get_navbar(html)

    top_items = {"Notice": top_notice, "News": top_news, "Events": top_events}
    footer = get_footer()
    return render_template(
        "home.html",
        top_items=top_items,
        footer=footer,
        nested_navs=nested_navs,
        main_navs=main_navs,
    )
