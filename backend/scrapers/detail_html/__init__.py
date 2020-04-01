"""
Detail html package:

get_responsive_html(url) -> [str] HTML
"""

import pandas as pd
from bs4 import BeautifulSoup as BS
from bs4 import Comment

from backend.scrapers import TRINITY_LINK, get_html

def remove_style_recursively(divs):
    for div in divs:
        div['style'] = ''
        if div.text and div.text.strip() == '·':
            div.extract()
        nested_divs = div.find_all('div')
        if len(nested_divs) != 0:
            remove_style_recursively(nested_divs)

def get_responsive_notice(url):
    """
    Wrapper around scrapers package get_html that returns responsive
    html from a url.
    Returns -> [str] HTML
    Params => [str] URL
    """
    html_soup = BS(get_responsive_html(url), features='lxml')
    # Fix MsoNormal divs (Notes div)
    msonormal_divs = html_soup.find_all('div', class_='MsoNormal')
    remove_style_recursively(msonormal_divs)

    # Fix tables
    try:
        dataframe = pd.read_html(url, header=0)
        html_soup = fix_notice_table(dataframe, html_soup)
    except Exception as e:
        print("ERROR:", e, url)

    return html_soup.prettify(formatter="html")


def get_responsive_news(url):
    pass


def get_responsive_events(url):
    pass


def get_responsive_html(url):
    """
    Wrapper around scrapers package get_html that returns responsive
    html from a url.
    Returns -> [str] HTML
    Params => [str] URL
    """
    html_obj = get_html(url, cache=False)
    # Get the downloadable item in left side
    content = html_obj.find("div#content", first=True)

    html_soup = BS(content.html, features="lxml")

    # Remove the comments in html
    comments = html_soup.find_all(string=lambda text: isinstance(text, Comment))
    for c in comments:
        c.extract()

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
                in_percentage = 100 / 20 * size
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
                image_url = url_part[4:-1]
                # http://test.com/images.png
                full_url = TRINITY_LINK + "/" + image_url
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
    html_soup = fix_table(html_soup)
    return html_soup.prettify(formatter="html")

def fix_table(html_soup):
    tables = html_soup.find_all("table")
    for index, table in enumerate(tables):
        table['class'] = 'table'
        table['style'] = ''
    return html_soup

def fix_notice_table(dataframe, html_soup):
    tables = html_soup.find_all("table")
    for index, table in enumerate(tables):
        table_dataframe = dataframe[index].to_html()
        new_table_tag = BS(table_dataframe, features="lxml").table
        class_attr = new_table_tag.get("class")
        new_table_tag["class"] = "tablesaw tablesaw-columntoggle"
        new_table_tag["data-tablesaw-mode"] = "columntoggle"

        thead = new_table_tag.thead
        head_ths = thead.find_all("th")
        for index, th in enumerate(head_ths):
            if th.text == "":
                th.extract()
            elif index == 1:
                th["data-tablesaw-priority"] = "persist"
            else:
                th["data-tablesaw-priority"] = str(index)
            th["scope"] = "col"
            th["data-tablesaw-sortable-column"] = ""

        tbody = new_table_tag.tbody
        body_ths = tbody.find_all("th")
        for th in body_ths:
            th.extract()

        table.replace_with(new_table_tag)


    return html_soup
