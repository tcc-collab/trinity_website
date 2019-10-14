"""
Detail html package:

get_responsive_html(url) -> [str] HTML
"""

from bs4 import BeautifulSoup as BS
from backend.scrapers import get_html


def get_responsive_html(url):
    """
    Wrapper around scrapers package get_html that returns responsive
    html from a url.
    Returns -> [str] HTML
    Params => [str] URL
    """
    html_obj = get_html(url)
    # Get the downloadable item in left side
    content = html_obj.find("div#content", first=True)

    html_soup = BS(content.html, features="lxml")

    # Make all ptags and span tags div
    all_p_tags = html_soup.find_all("p")
    for p_tag in all_p_tags:
        p_tag.name = "div"

    all_span_tags = html_soup.find_all("span")
    for span_tag in all_span_tags:
        span_tag.name = "div"

    all_divs = html_soup.find_all("div")

    # Remove the troubling width attr in style attr
    for div in all_divs:
        style_attr = div.attrs.get("style")
        if not style_attr:
            continue

        style_attr = style_attr
        styles = style_attr.split(";")
        styles_copy = styles[:]
        for style in styles_copy:
            if "width" in style:
                styles.remove(style)

            # Convert font-size from px/pt to em (formula 1/16 * px = em)
            if "font-size" in style:
                css_style = style.strip()
                name_part = css_style.split(":")[0]
                size_part = css_style.split(":")[1].strip()
                last_num = list(filter(str.isdigit, size_part))[-1]
                size = int(float(size_part[: size_part.rfind(last_num) + 1]))
                in_percentage = 100 / 16 * size
                if in_percentage > 200:
                    in_percentage = 200
                em_size_part = str(in_percentage) + "%"
                new_style = name_part + ":" + em_size_part
                styles.remove(style)
                styles.append(new_style)

        style_attr = "; ".join(styles)
        div["style"] = style_attr

    # Put container fluid in all the divs
    for div in all_divs:
        div_class = div.get("class")
        """
        if not div_class:
            div["class"] = "container-fluid container2"
        else:
            div["class"] += " container-fluid container2"
            """

    return html_soup.prettify(formatter="html")
