"""
Footer package:

get_footer(html) -> Dict
"""


def get_footer(html_soup):
    """
    Params -> <requests HTML> obj
    Returns -> Dict {
    'privacy_policy': link to site's privacy policy
    'disclaimer': link to site's disclaimer
    'youtube': trinity's youtube channel
    'twitter': trinity's twitter handle
    'facebook': trinity's facebook page
    }
    """
    footer_div = html_soup.find("#footer", first=True)
    legal_div = footer_div.find("div", first=True)
    a_tags = legal_div.find("a")

    privacy_policy = a_tags[0].attrs.get("href")
    disclaimer = a_tags[1].attrs.get("href")
    privacy_policy_link = html_soup.url + "/" + privacy_policy
    disclaimer_link = html_soup.url + "/" + disclaimer

    # TODO For now social media links are hardcoded :)
    facebook = "https://www.facebook.com/"
    trinity_fb_id = "Trinity-International-HSSCollege-123877371368846/?fref=ts"
    youtube_link = "https://www.youtube.com/channel/UCI9QxocOF5Dy5_skkOYIGiA"
    twitter_link = "https://twitter.com/TrinityHSSchool"

    footer_items = {
        "privacy_policy": privacy_policy_link,
        "disclaimer": disclaimer_link,
        "youtube": youtube_link,
        "twitter": twitter_link,
        "facebook": facebook + trinity_fb_id,
    }

    return footer_items
