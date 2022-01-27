from jina import Client, Document
from config import DATA_DIR, TEXT_PORT, TEXT_SERVER, IMAGE_PORT, IMAGE_SERVER, TOP_K
from PIL import Image
import numpy as np 

class UI:
    about_block = """

    ### About

    This is a meme search engine using [Jina's neural search framework](https://github.com/jina-ai/jina/).

    - [Live demo](https://examples.jina.ai/memes)
    - [Play with it in a notebook](https://colab.research.google.com/github/jina-ai/workshops/blob/main/memes/meme_search.ipynb) (text-only)
    - [Repo](https://github.com/alexcg1/jina-meme-search)
    - [Dataset](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset)
    """

    css = f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
"""


headers = {"Content-Type": "application/json"}
def load_image(img):
    im = Image.open(img)
    image = np.array(im)
    return image


def search_by_text(input, server=TEXT_SERVER, port=TEXT_PORT, limit=TOP_K):
    client = Client(host=server, protocol="http", port=port)
    response = client.search(
        Document(text=input),
        parameters={"limit": limit},
        return_results=True,
        show_progress=True,
    )
    matches = response[0].docs[0].matches

    return matches


def search_by_file(document, server=IMAGE_SERVER, port=IMAGE_PORT, limit=TOP_K):
    """
    Wrap file in Jina Document for searching, and do all necessary conversion to make similar to indexed Docs
    """
    client = Client(host=server, protocol="http", port=port)
    query_doc = document
    response = client.search(
        query_doc,
        parameters={"limit": 20},
        return_results=True,
        show_progress=True,
    )
    matches = response[0].docs[0].matches
    return matches


def convert_file_to_document(query):
    data = query.read()
    print(data)
    with open("/home/souvik/Documents/ikea-search/test_images/images.jpg", "wb") as file:
        file.write(data)
    doc = Document(uri="/home/souvik/Documents/ikea-search/test_images/images.jpg")
    print(doc.uri)
    return doc


def get_image_url(file_path):
    return file_path
