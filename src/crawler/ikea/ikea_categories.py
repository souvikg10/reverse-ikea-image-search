from typing import Dict
from bs4 import BeautifulSoup
import requests
from src.db.sql_model import get_session, ProductSubCategory
import pandas as pd


class FetchIkeaCategories:
    def __init__(self, url) -> None:
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.session = get_session()

    def get_categories(self):
        my_categories = self.soup.find_all("span", class_="hnf-menu__heading")
        categories = []
        for cat in my_categories:
            categories.append(cat.getText())
        return categories

    def get_sub_categories(self):
        list_items = self.soup.find_all("li")
        sub_categories = []
        for item in list_items:
            anchor = item.find_all("a", class_="hnf-link")[0]
            category_id = anchor.get("data-tracking-label")
            category_name = anchor.getText()
            sub_categories.append(
                {"category_id": category_id, "category_name": category_name}
            )
            sub_categories = [
                i
                for i in sub_categories
                if not (i["category_id"] == "all" or i["category_id"] == None)
            ]
        return sub_categories

    def prepare_sub_category_datatable(
        self, sub_category: Dict, language: str, region: str
    ):
        df = pd.DataFrame.from_dict(sub_category)
        for index, row in df.iterrows():
            data_insert = ProductSubCategory(
                sub_category_name=row["category_name"],
                sub_category_id=row["category_id"],
                language=language,
                region=region,
            )
            self.session.add(data_insert)
        self.session.commit()
