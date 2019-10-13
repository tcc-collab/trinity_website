"""
Notice package:
get_top_notice -> [List] list of recent 3 notices[type dict]
notice_page_link -> [str] link of notice page containing all notices
get_all_notice -> [List] list of all notices[type dict]
"""

from backend.scrapers.notice.main import (
    get_all_notice,
    get_top_notice,
    notice_page_link,
)
