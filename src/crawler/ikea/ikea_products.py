from typing import Dict, List
import requests
import pandas as pd
from src.db.sql_model import get_session, Products


class FetchProductsByCategory:
    def __init__(self) -> None:
        self.session = get_session()

    def fetch_products_list(self, category: str, language: str, region: str) -> List:
        json = requests.get(
            f"https://sik.search.blue.cdtapps.com/{region}/{language}/product-list-page?category={category}&size=2000"
        ).json()["productListPage"]["productWindow"]
        return json

    def get_all_image_url(self, product_item) -> List:
        alternative_image_urls = []
        alternative_images = product_item.get("variants")
        for images in alternative_images:
            alternative_image_urls.append(images.get("imageUrl"))
        return alternative_image_urls

    def prepare_product_datatable(
        self, product_list: Dict, language: str, region: str, category: str
    ):
        df = pd.DataFrame.from_dict(product_list)
        for index, row in df.iterrows():
            data_insert = Products(
                name=row["name"],
                type_name=row["typeName"],
                price=row["priceNumeral"],
                currency_code=row["currencyCode"],
                product_url=row["pipUrl"],
                image_url=row["mainImageUrl"],
                alternative_image_urls=str(
                    self.get_all_image_url(row["gprDescription"])
                ),
                discount=row["discount"],
                language=language,
                region=region,
                sub_category_id=category,
            )
            self.session.add(data_insert)
        self.session.commit()
