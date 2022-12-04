from linkpreview.preview.metabase import MetaPreviewBase


class OpenGraph(MetaPreviewBase):
    """
    Gets OpenGraph meta properties of a webpage.
    sample: <meta property="og:title" content="blabla">
    """

    __target_attr__ = "property"

    @property
    def title(self):
        return self._get_property("og:title")

    @property
    def description(self):
        return self._get_property("og:description")

    @property
    def image(self):
        return self._get_property("og:image")
