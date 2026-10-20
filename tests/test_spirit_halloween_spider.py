import json

from scrapy.http import TextResponse

from locations.spiders.spirit_halloween import SpiritHalloweenSpider

# Records trimmed from the Rio SEO getAsyncLocations response.
LOCATIONS = [
    {
        "fid": "61117",
        "url": "https://stores.spirithalloween.com/ca/salinas/halloween-store-61117.html",
        "location_name": "Salinas Northridge",
        "address_1": "370 Northridge Mall",
        "address_2": "",
        "city": "Salinas",
        "region": "CA",
        "post_code": "93906",
        "lat": "36.7148824936687",
        "lng": "-121.66057058500",
        "local_phone": "(855) 704-2669",
        "location_address_description": "",
    },
    {
        "fid": "65010",
        "url": "https://stores.spirithalloween.com/me/auburn/halloween-store-65010.html",
        "location_name": "Auburn ME",
        "address_1": "550 Center  Street",
        "address_2": "Suite 1114 & 116",
        "city": "Auburn",
        "region": "ME",
        "post_code": "04210",
        "lat": "44.1225244553697",
        "lng": "-70.231426436102",
        "local_phone": "(855) 704-2669",
        "location_address_description": "Next to Classic Amusements",
    },
    {
        "fid": "65090",
        "url": "https://stores.spirithalloween.com/me/waterville/halloween-store-65090.html",
        "location_name": "Waterville",
        "address_1": "180 JFK Plaza",
        "address_2": "",
        "city": "Waterville",
        "region": "ME",
        "post_code": "04901",
        "lat": "44.5399519156105",
        "lng": "-69.652162873922",
        "local_phone": "(855) 704-2669",
        "location_address_description": "Former JoAnn",
    },
]


def parse_locations() -> dict:
    map_list = '<div class="tlsmap_list">' + ",".join(json.dumps(location) for location in LOCATIONS) + ",</div>"
    response = TextResponse(
        url="https://maps.spirithalloween.com/api/getAsyncLocations",
        body=json.dumps({"maplist": map_list}),
        encoding="utf-8",
    )
    return {item["ref"]: item for item in SpiritHalloweenSpider().parse(response)}


def test_location_hint_is_appended_to_street_address():
    item = parse_locations()["65090"]
    assert item["street_address"] == "180 JFK Plaza, Former JoAnn"
    assert item["branch"] == "Waterville"
    assert item["website"] == "https://stores.spirithalloween.com/me/waterville/halloween-store-65090.html"


def test_location_hint_follows_address_line_two():
    item = parse_locations()["65010"]
    assert item["street_address"] == "550 Center  Street, Suite 1114 & 116, Next to Classic Amusements"


def test_store_without_location_hint():
    item = parse_locations()["61117"]
    assert item["street_address"] == "370 Northridge Mall"
