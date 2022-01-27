from jina import DocumentArray, Executor, Flow, requests
import torchvision


class PreprocImg(Executor):
    @requests(on="/search")
    def foo(self, docs: DocumentArray, **kwargs):
        for d in docs:
            (
                d.load_uri_to_image_blob(width=224, height=224)
                .set_image_blob_normalization()  # normalize color
                .set_image_blob_channel_axis(-1, 0)
            )  # switch color axis


class EmbedImg(Executor):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.model = torchvision.models.resnet50(pretrained=True)

    @requests(on="/search")
    def foo(self, docs: DocumentArray, **kwargs):
        docs.embed(self.model, device="cuda", batch_size=100)


class MatchImg(Executor):
    _da = DocumentArray().load_binary("embeddings/index.bin")

    @requests(on="/search")
    def foo(self, docs: DocumentArray, **kwargs):
        docs.match(self._da)
        for d in docs.traverse_flat("r,m"):  # only require for visualization
            d.convert_uri_to_datauri()
            d.pop("embedding", "blob")  # remove unnecessary fields for save bandwidth


f = (
    Flow(port_expose=12345, protocol="http")
    .add(uses=PreprocImg)
    .add(uses=EmbedImg, replicas=3)
    .add(uses=MatchImg)
)
f.plot("f.png")

with f:
    f.block()
