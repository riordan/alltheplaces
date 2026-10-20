from typing import Iterable

from locations.items import Feature
from locations.pipelines.address_clean_up import merge_address_lines
from locations.storefinders.rio_seo import RioSeoSpider


class SpiritHalloweenSpider(RioSeoSpider):
    name = "spirit_halloween"
    item_attributes = {"brand": "Spirit Halloween", "brand_wikidata": "Q25212133"}
    end_point = "https://maps.spirithalloween.com"

    def post_process_feature(self, feature: Feature, location: dict) -> Iterable[Feature]:
        feature["branch"] = feature.pop("name")
        # Location hint such as "Former JoAnn" or "Next to Target".
        feature["street_address"] = merge_address_lines(
            [feature["street_address"], location.get("location_address_description")]
        )
        yield feature
