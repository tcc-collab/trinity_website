"""
Navigation: main.py module
"""


def get_side_nav_menu(html_soup):
    """
    Returns -> [list] list of side navigation menus[type dict]
      Menu -> [Dict] attrs:
        'name' -> [str] name of menu
        'link' -> [str] link for the menu
        'image' -> [str] URL for menu image

    Params -> [requests.HTML object] HTML of web page.
    """
    # Container ul with all navigation menus
    menu_div = html_soup.find("ul#suckertree1", first=True)

    # list of divs containing menu title and link
    menu_items = menu_div.find("li")
    side_menus = []

    for menu in menu_items:
        menu_a_tag = menu.find("a", first=True)
        name = menu_a_tag.text
        link = menu_a_tag.attrs.get("href")
        full_link = html_soup.url + link
        image = menu.find("img", first=True).attrs.get("src")
        # image_link = html_soup.url + image
        menu_dict = {"name": name, "link": full_link, "image": image}
        side_menus.append(menu_dict)

    print(side_menus)
    return side_menus


def get_main_nav_menu(html_soup):
    """
    Returns -> [list] list of all main menus[type dict]
      Menu -> [Dict] attrs:
        'name' -> [str] name of menu
        'link' -> [str] link for the menu
        'image' -> [str] URL for menu image

    Params -> [requests.HTML object] HTML of web page.
    """

    all_menu_div = html_soup.find("div#chromemenu", first=True)
    main_menu_ul = all_menu_div.find("ul", first=True)
    menu_li_items = main_menu_ul.find("li")
    all_menu = []

    for li_tag in menu_li_items:
        a_tag = li_tag.find("a", first=True)
        name = a_tag.text
        link = a_tag.attrs.get("href").strip()
        if link == "#":
            menu_rel = a_tag.attrs.get("rel")[0]
            name, link = __extract_dropdowns(html_soup, menu_rel)

        full_link = f"{html_soup.url}/{link.strip()}"
        menu_dict = {"name": name, "link": full_link}
        all_menu.append(menu_dict)

    return all_menu


def __extract_dropdowns(html_soup, menu):
    css_selector = f"div#{menu}"
    menu_div = html_soup.find(css_selector, first=True)
    a_tag = menu_div.find("a", first=True)
    name = a_tag.text[2:]
    link = a_tag.attrs.get("href")
    return name, link
