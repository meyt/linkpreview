from linkpreview.preview.metabase import MetaPreviewBase


class Microdata(MetaPreviewBase):
    """
    Schema.org meta properties
    sample: <meta itemprop="name" content="blabla">
    """

    __target_attr__ = "itemprop"

    @property
    def title(self):
        return self._get_property("name")

    @property
    def description(self):
        return self._get_property("description")

    @property
    def image(self):
        return self._get_property("image")
