from unicodedata import category
from src.crawler.ikea.ikea_products import FetchProductsByCategory
from src.crawler.ikea.ikea_categories import FetchIkeaCategories


if __name__ == "__main__":
    cat = FetchIkeaCategories(
        url="https://www.ikea.com/be/fr/header-footer/menu-products.html"
    )
    categories = cat.get_sub_categories()
    cat.prepare_sub_category_datatable(categories, language="fr", region="be")
    prod = FetchProductsByCategory()
    for c in categories:
        products = prod.fetch_products_list(
            category=c["category_id"], language="fr", region="be"
        )
        prod.prepare_product_datatable(
            products, language="fr", region="be", category=c["category_id"]
        )
