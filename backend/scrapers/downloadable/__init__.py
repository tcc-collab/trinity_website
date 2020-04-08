"""
Downloadable package:

get_downloadable(html) -> Dict
"""
from bs4 import BeautifulSoup as BS

def get_downloadable(html):
    """
    Params = <reuests HTML> obj
    Returns -> Dict{
    'left': Dict {
          'link': Link of downloadable item
          'caption': Short description of item
         }
    }
    """
    soup = BS(html.html, features='lxml')
    get_full_link = lambda x:f"{html.url}/{x.strip()}"

    # Get the downloadable item in left side
    left_div = soup.find("div", id="leftnoav")
    left_div_a_tag = left_div.p.a

    link = left_div_a_tag.attrs.get("href")
    left_link = get_full_link(link) if 'http' not in link else link.strip()

    left_img = left_div_a_tag.img.attrs.get('src')
    left_img_link = get_full_link(left_img) if 'http' not in left_img else left_img.strip()

    left_title = left_div_a_tag.string
    if not left_img_link and not left_title:
        left_title = link
    elif left_img_link and not left_title:
        left_title = ''

    # Get the downloadable item in right side
    right_div = soup.find("div", id="round_bottom_left")
    right_div_a_tag = right_div.find_next('a')
    link = right_div_a_tag.attrs.get("href")
    right_link = get_full_link(link) if 'http' not in link else link.strip()

    right_img = right_div_a_tag.find('img').attrs.get('src')
    right_img_link = get_full_link(right_img) if 'http' not in right_img else right_img.strip()

    right_title = right_div_a_tag.string
    if not right_img_link and not right_title:
        right_title = link
    elif right_img_link and not right_title:
        right_title = ""

    downloadables = {
        "left": {"link": left_link, "caption": left_title, "image":left_img_link},
        "right": {'link': right_link, 'caption': right_title, "image":right_img_link},
    }
    return downloadables
