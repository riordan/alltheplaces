from typing import Iterable

from scrapy.http import Response

from locations.categories import Categories, apply_category
from locations.items import Feature
from locations.storefinders.storefrontgateway import StorefrontgatewaySpider


class KingKullenUSSpider(StorefrontgatewaySpider):
    name = "king_kullen_us"
    item_attributes = {"brand": "King Kullen", "brand_wikidata": "Q6411832"}
    start_urls = ["https://storefrontgateway.kingkullen.com/api/stores"]
    requires_proxy = "US"  # Cloudflare geoblocking in use

    def post_process_item(self, item: Feature, response: Response, location: dict) -> Iterable[Feature]:
        apply_category(Categories.SHOP_SUPERMARKET, item)
        yield item
