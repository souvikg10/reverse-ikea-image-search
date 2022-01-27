from jina import Document, DocumentArray
import os
import torchvision


def createDocumentArray(images):
    da = DocumentArray(
        (Document(uri=name, tags={"file": {"file_name": name}}) for name in images)
    )
    return da


def preprocess(d):
    return (
        d.load_uri_to_image_blob(width=224, height=224)
        .set_image_blob_normalization()  # normalize color
        .set_image_blob_channel_axis(-1, 0)
    )  # switch color axis


def init_resnet50():
    model = torchvision.models.resnet50(pretrained=True)
    return model


def embed(docs: DocumentArray, model):
    docs.embed(model, device="cuda", batch_size=100)
    return docs


def save(docs: DocumentArray):
    docs.save_binary("embeddings/index.bin")


def load():
    docs = DocumentArray().load_binary("embeddings/index.bin")
    return docs


if __name__ == "__main__":
    list_of_files = []
    for root, dirs, files in os.walk("images/"):
        for file in files:
            list_of_files.append(os.path.join(root, file))
    list_of_files = sorted(list_of_files)
    docs = createDocumentArray(list_of_files)
    docs.apply(preprocess)
    model = init_resnet50()
    docs = embed(docs, model)
    save(docs)
