"""
Detail html package:

get_responsive_html(url) -> [str] HTML
"""

from bs4 import BeautifulSoup as BS
from backend.scrapers import get_html, TRINITY_LINK


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
        styles = [i for i in styles if i]
        styles_copy = styles[:]
        for style in styles_copy:
            if "width" in style:
                styles.remove(style)

            # Convert font-size from px/pt to em (formula 1/16 * px = em)
            if "font-size" in style:
                # font-size : 15.5px;
                css_style = style.strip()
                name_part = css_style.split(":")[0]
                size_part = css_style.split(":")[1].strip()

                # 5
                last_num = list(filter(str.isdigit, size_part))[-1]
                # 5 -> index=1,3 -> index=3 -> '15.5' -> 15.5 -> 15
                size = int(float(size_part[: size_part.rfind(last_num) + 1]))
                in_percentage = 100 / 16 * size
                if in_percentage > 200:
                    in_percentage = 200
                em_size_part = str(in_percentage) + "%"
                new_style = name_part + ":" + em_size_part
                styles.remove(style)
                styles.append(new_style)

            if "background-image" in style:
                # background-image : url(images.png)
                background_image = style.strip()
                # url(images.png)
                url_part = background_image.split(":")[1].strip()
                # images.png
                url = url_part[4:-1]
                # http://test.com/images.png
                full_url = TRINITY_LINK + "/" + url
                new_style = f"background-image:url({full_url})"
                styles.remove(style)
                styles.append(new_style)

        style_attr = "; ".join(styles)
        div["style"] = style_attr

    # Fix images src url
    img_tags = html_soup.find_all("img")
    for img_tag in img_tags:
        src_attr = img_tag.attrs.get("src")
        if src_attr and not src_attr.strip().startswith("data:"):
            img_tag["src"] = TRINITY_LINK + "/" + src_attr

    # Fix images href of a_tags
    a_tags = html_soup.find_all("a")
    for a_tag in a_tags:
        href_attr = a_tag.attrs.get("href")
        if href_attr and not href_attr.strip().startswith("#"):
            a_tag["href"] = TRINITY_LINK + "/" + href_attr

    # Fix tables
    tables = html_soup.find_all("table")
    for table in tables:
        class_attr = table.get("class")
        if class_attr:
            table["class"] += " responsive"
        else:
            table["class"] = "responsive"

        style_attr = table.get("style")
        if style_attr:
            del table["style"]

        table_tags = table.find_all()
        for tag in table_tags:
            style_attr = tag.get("style")
            if style_attr:
                del tag["style"]
            width_attr = tag.get("width")
            if width_attr:
                del tag["width"]

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
