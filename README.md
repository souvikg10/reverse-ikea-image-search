# IKEA Reverse Image Search

This is a demo project to fetch ikea product images(IKEA Copyrights them so can only be used for private purposes). 

MUST read their terms and conditions before using their iamges for anything other than private purposes.

## You must have a virtual environment

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

```

## Download Product Data and prepare 

First script to run that creates the database in sqllite

```sh
python src/db/sql_model.py
```
Then prepare_data
```sh
python prepare_data.py
```

*Note i am pulling the data from IKEA Belgium's French website because that's where i am. You can modify this in the script to the location you are in.*

Now Download imags(This can take long)
```
python download_images.py
```

if you are interested in downloading just one of the categories.
First look up the database to check category_id for the category you want in the ProductSubcategory Table, then open 

`download_images.py`

modify this function call
```
DownloadImage.download_product_images(
        base_image_dir, language=language, region=region
    )
```
to
```
DownloadImage.download_product_images_by_category(
        base_image_dir, language=language, region=region, category_id = "fu003"(category for couches, you can change this)
    )
```

## Index
Run 
```
python index.py
```

This will index all the images based on resnet50

## Search
Run the server to enable a search endpoint
```
python search.py

```

## Frontend
Run the streamlit app
```
cd frontend
streamlit run frontend.py
```

This will open the browser to the streamlit app. 