"""
Notice: main.py module
"""


def notice_page_link(html_soup):
    """
    Returns -> [str] link of notice page.
    Params -> [requests.HTML object] HTML of web page.
    """
    notice_div_xpath = "/html/body/div/div[2]/div[1]/div[6]/div"
    # Container div with all top notices and p tag(at last) with more link
    notice_div = html_soup.xpath(notice_div_xpath, first=True)

    more_notices_p_tag = notice_div.find("p")[-1]
    more_notices_a_tag = more_notices_p_tag.find("a", first=True)
    more_notices_link = html_soup.url + more_notices_a_tag.attrs["href"]
    return more_notices_link


def get_top_notice(html_soup):
    """
    Returns -> [list] list of latest 3 notices
      Notice -> [Dict] attrs:
        'title' -> [str] title of notice
        'link' -> [str] full link for the notice

    Params -> [requests.HTML object] HTML of web page.
    """
    notice_div_xpath = "/html/body/div/div[2]/div[1]/div[6]/div"
    # Container div with all top notices
    notice_div = html_soup.xpath(notice_div_xpath, first=True)

    # list of divs containing notice title and link
    notices = notice_div.find("div.notic_text")
    top_notices = []

    for notice in notices:
        title = notice.text
        link = notice.find("a", first=True).attrs.get("href")
        full_link = html_soup.url + link
        notice_dict = {"title": title, "full_link": full_link}
        top_notices.append(notice_dict)

    return top_notices


def get_all_notice(html_soup):
    """
    Returns -> [list] list of all notices
      Notice -> [Dict] attrs:
        'title' -> [str] title of notice
        'link' -> [str] full link for the notice
        'date' -> [str] Date of notice eg:
        'content' -> [str] short summary of notice
        [Note: content = 'Notice' or 5/6 words string most of time]

    Params -> [requests.HTML object] HTML of web page.
    """
    all_notice_div = html_soup.find("div#content_text", first=True)
    notices = all_notice_div.find("div#news")

    more_notices = []
    for notice in notices:
        date = notice.find("div.date", first=True).text
        content = notice.find("div.content", first=True).text
        title_div = notice.find("div.title1", first=True)
        title = title_div.find("a", first=True).text
        link_div = notice.find("div.more", first=True)
        link = html_soup.url + link_div.find("a", first=True).attrs.get("href")

        notice_dict = {"date": date, "title": title, "content": content, "link": link}
        more_notices.append(notice_dict)

    return more_notices
