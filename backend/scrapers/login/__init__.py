"""
Login package:
get_login_captcha -> [str] math captcha in login.
"""

from backend.scrapers import get_html


def get_login_captcha():
    """
    Returns -> [str] math captcha in login.
    """
    html_soup = get_html()
    login_captcha_xpath = (
        "/html/body/div/div[2]/div[2]/div[3]/div[2]/form/div[4]/div[1]"
    )
    captcha_str = html_soup.xpath(login_captcha_xpath, first=True).text
    return captcha_str
