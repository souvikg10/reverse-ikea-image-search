from typing import List, Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select


class Products(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type_name: str
    price: float
    currency_code: str
    product_url: str
    image_url: str = None
    alternative_image_urls: str = None
    discount: str = None
    language: str = None
    region: str = None
    sub_category_id: Optional[str] = Field(
        default=None, foreign_key="productsubcategory.sub_category_id"
    )


def select_products(language, region, sub_category_id) -> List:
    with get_session() as session:
        statement = (
            select(Products)
            .where(Products.language == language)
            .where(Products.region == region)
            .where(Products.sub_category_id == sub_category_id)
        )
        results = session.exec(statement)
        return results.all()


class ProductSubCategory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sub_category_name: str
    sub_category_id: str
    language: str
    region: str


def select_product_category(language, region) -> List:
    with get_session() as session:
        statement = (
            select(ProductSubCategory)
            .where(ProductSubCategory.language == language)
            .where(ProductSubCategory.region == region)
        )
        results = session.exec(statement)
        return results.all()


def get_engine():
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url)
    return engine


def get_session():
    session = Session(get_engine())
    return session


def create_db_and_tables():  #
    SQLModel.metadata.create_all(get_engine())  #


if __name__ == "__main__":
    create_db_and_tables()
