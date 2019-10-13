from backend.scrapers.navigation import get_main_nav_menu, get_side_nav_menu


def get_navbar(html):
    side_navs = get_side_nav_menu(html)
    gallery = {"Gallery": []}
    publication = []
    for nav_item in side_navs:
        if nav_item["name"] == "Publications":
            publication.append(nav_item)

        elif nav_item["name"] == "Photo Gallery" or nav_item["name"] == "Video Gallery":
            gallery["Gallery"].append(nav_item)

    nav_items = [publication[0], gallery]
    return nav_item
