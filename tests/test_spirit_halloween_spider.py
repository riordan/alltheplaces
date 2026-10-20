# ABOUTME: Tests the Spirit Halloween spider store page parser against saved store page fixtures.
# ABOUTME: Checks that the store's own address line two (e.g. "Former JoAnn") is kept in the address.
from scrapy.http import HtmlResponse

from locations.spiders.spirit_halloween import SpiritHalloweenSpider


def parse_fixture(name: str, url: str):
    with open(f"./tests/data/spirit_halloween_{name}.html") as f:
        response = HtmlResponse(url=url, body=f.read(), encoding="utf-8")
    return SpiritHalloweenSpider().parse_stores(response)


def test_address_line_two_is_appended_to_address():
    item = parse_fixture("waterville", "https://stores.spirithalloween.com/me/waterville/halloween-store-65090.html")
    assert item["addr_full"] == "180 JFK Plaza, Former JoAnn"
    assert item["city"] == "Waterville"


def test_address_line_two_of_nearby_stores_is_ignored():
    item = parse_fixture("salinas", "https://stores.spirithalloween.com/ca/salinas/halloween-store-61117.html")
    assert item["addr_full"] == "370 Northridge Mall"
