"""
Events package:
get_top_event -> [List] list of recent 3 notices[type dict]
event_page_link -> [str] link of notice page containing all notices
"""

from backend.scrapers.events.main import event_page_link, get_top_event
