from flask import Flask, render_template

from backend.scrapers import get_html
from backend.scrapers.downloadable import get_downloadable
from backend.scrapers.events import event_page_link, get_top_event
from backend.scrapers.footer import get_footer
from backend.scrapers.navigation import get_main_nav_menu, get_side_nav_menu
from backend.scrapers.news import get_all_news, get_top_news, news_page_link
from backend.scrapers.notice import get_all_notice, get_top_notice, notice_page_link


app = Flask(__name__)


@app.route("/")
def event():
    url = "http://trinitycollege.edu.np"
    html = get_html(url=url)
    top_notice = get_top_notice(html)
    top_events = get_top_event(html)
    top_news = get_top_news(html)
    top_items = [top_notice, top_events, top_news]
    return render_template("layout.html", top_items=top_items)
