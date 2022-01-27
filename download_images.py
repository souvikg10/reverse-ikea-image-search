from src.db.sql_model import select_products, select_product_category
import os
import requests
import ast


class DownloadImage:
    def __init__(self) -> None:
        pass

    @staticmethod
    def download_product_images_by_category(
        image_dir: str, language: str, region: str, category_id: str
    ):
        productbycategory = select_products(
            language=language, region=region, sub_category_id=category_id
        )
        for product in productbycategory:
            if not os.path.exists(image_dir + "/" + product.name):
                print("creating folder:" + product.name)
                os.makedirs(image_dir + "/" + product.name)
                image_name = product.image_url.split("/")[-1]
                img_data = requests.get(product.image_url).content
                print(
                    "download image at: "
                    + image_dir
                    + "/"
                    + product.name
                    + "/"
                    + image_name
                )
                with open(
                    image_dir + "/" + product.name + "/" + image_name, "wb"
                ) as handler:
                    handler.write(img_data)
                if not product.alternative_image_urls == "[]":
                    for image in ast.literal_eval(product.alternative_image_urls):

                        file_name = image.split("/")[-1]
                        print(
                            "download image at: "
                            + image_dir
                            + "/"
                            + product.name
                            + "/"
                            + file_name
                        )
                        img = requests.get(image).content
                        with open(
                            image_dir + "/" + product.name + "/" + file_name, "wb"
                        ) as handler:
                            handler.write(img)
            else:
                continue

    def count_total_product_images(self, language: str, region: str):
        category = select_product_category(language=language, region=region)
        images = []
        for cat in category:
            productbycategory = select_products(language, region, cat.sub_category_id)
            for product in productbycategory:
                images.append(product.image_url)
                if not product.alternative_image_urls == "[]":
                    for image in ast.literal_eval(product.alternative_image_urls):
                        images.append(image)
        return images

    @staticmethod
    def download_product_images(image_dir: str, language: str, region: str):
        category = select_product_category(language=language, region=region)
        for cat in category:
            productbycategory = select_products(language, region, cat.sub_category_id)
            for product in productbycategory:
                if not os.path.exists(image_dir + "/" + product.name):
                    print("creating folder:" + product.name)
                    os.makedirs(image_dir + "/" + product.name)
                    image_name = product.image_url.split("/")[-1]
                    img_data = requests.get(product.image_url).content
                    print(
                        "download image at: "
                        + image_dir
                        + "/"
                        + product.name
                        + "/"
                        + image_name
                    )
                    with open(
                        image_dir + "/" + product.name + "/" + image_name, "wb"
                    ) as handler:
                        handler.write(img_data)
                    if not product.alternative_image_urls == "[]":
                        for image in ast.literal_eval(product.alternative_image_urls):

                            file_name = image.split("/")[-1]
                            print(
                                "download image at: "
                                + image_dir
                                + "/"
                                + product.name
                                + "/"
                                + file_name
                            )
                            img = requests.get(image).content
                            with open(
                                image_dir + "/" + product.name + "/" + file_name, "wb"
                            ) as handler:
                                handler.write(img)
                else:
                    continue


if __name__ == "__main__":
    language = "fr"
    region = "be"
    base_image_dir = f"images/"
    if not os.path.exists(base_image_dir):
        os.makedirs(base_image_dir)
    DownloadImage.download_product_images(
        base_image_dir, language=language, region=region
    )
