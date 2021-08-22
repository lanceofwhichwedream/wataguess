import requests
import re
from bs4 import BeautifulSoup

test_regex = re.compile(r"([A-Za-z0-9:/.]*[?][_A-Za-z=0-9%-.]*)")


def clean_url(url):
    """clean_url

    I'm not a fan of url gore so this is to clean that up

    :param url: Represents a url, assumed to be an ebay url
    :type url: String
    :return: Cleaned up version of the url
    :rtype: String
    """
    if test_regex.search(url):
        url = url.split("?")

    return url[0]


def get_data(url):
    """Scraps the information from the ebay url

    :param url: URL of the item in question
    :type url: String
    """
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    price = soup.find("span", {"class": "notranslate"}).get_text().split("$")[1]
    item = soup.find("meta", {"property": "og:title"})["content"]
    item_id = url.split("itm/")[1]

    return item, price, item_id
