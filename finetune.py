from docarray import DocumentArray, Document
import os


def createDocumentArray(images):
    da = DocumentArray(
        (Document(uri=name, tags={"file": {"file_name": name}}) for name in images)
    )
    return da


list_of_files = []
for root, dirs, files in os.walk("couch_images"):
    for file in files:
        list_of_files.append(os.path.join(root, file))
list_of_files = sorted(list_of_files)
print(len(list_of_files))
data = createDocumentArray(list_of_files)


def preproc(doc):
    return (
        doc.load_uri_to_image_blob(224, 224)
        .set_image_blob_normalization()
        .set_image_blob_channel_axis(-1, 0)
    )


data.apply(preproc)

import torchvision

resnet = torchvision.models.resnet50(pretrained=True)

import gc
import torch

gc.collect()
torch.cuda.empty_cache()

import finetuner as ft

tuned_model = ft.fit(
    resnet,
    train_data=data,
    interactive=True,
    to_embedding_model=False,
    freeze=False,
    input_size=(3, 224, 224),
)
ft.save(tuned_model, "tuned-model")
