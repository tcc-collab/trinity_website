"""
Downloadable package:

get_downloadable() -> Dict
"""

from backend.scrapers import get_html


def get_downloadable():
    """
    Returns -> Dict{
    'left': Dict {
          'link': Link of downloadable item
          'caption': Short description of item
         }
    }
    """
    html_soup = get_html()

    # Get the downloadable item in left side
    left_div = html_soup.find("div#leftnoav", first=True)
    left_div_a_tag = left_div.find("p", first=True).find("a", first=True)

    left_title = left_div_a_tag.text
    link = left_div_a_tag.attrs.get("href")
    left_link = f"{html_soup.url}/{link.strip()}"

    # TODO Get the downloadable item in Right side

    downloadables = {
        "left": {"link": left_link, "caption": left_title},
        # 'right': {'link': left_link, 'title': title},
    }

    return downloadables
