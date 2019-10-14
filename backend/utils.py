from backend.scrapers.navigation import get_main_nav_menu, get_side_nav_menu


def get_navbar(html):
    side_navs = get_side_nav_menu(html)
    main_navs = get_main_nav_menu(html)

    publication, contact, admission = None, None, None
    home = {"name": "Home", "link": "{{url_for(home)}}"}
    deep_navs = {"Gallery": [], "Faculty and staffs": [], "Academic Programs": []}

    for nav_item in main_navs:
        nav_name = nav_item["name"].lower()
        if "contact" in nav_name:
            contact = nav_item

        elif "admission" in nav_name:
            admission = nav_item

        elif "+2" in nav_name or "a level" in nav_name or "TU" in nav_item["name"]:
            deep_navs["Academic Programs"].append(nav_item)

    for nav_item in side_navs:
        nav_name = nav_item["name"].lower()
        if "publication" in nav_name:
            publication = nav_item

        elif "photo" in nav_name or "video" in nav_name:
            deep_navs["Gallery"].append(nav_item)

        elif "board" in nav_name or "team" in nav_name or "faculty" in nav_name:
            if "&" not in nav_name and "and" not in nav_name:
                deep_navs["Faculty and staffs"].append(nav_item)

    top_navs = [home, contact, publication, admission]
    return (top_navs, deep_navs)


# def get_responsive_html(url):
#    html_soup = get_html(url)
#    url_div_map = {}
