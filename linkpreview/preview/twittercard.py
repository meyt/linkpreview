from linkpreview.preview.metabase import MetaPreviewBase


class TwitterCard(MetaPreviewBase):
    """
    Gets TwitterCard meta properties of a webpage.
    sample: <meta name="twitter:title" content="blabla">
    """

    __target_attr__ = "name"

    @property
    def site_name(self):
        # not supported
        return

    @property
    def title(self):
        return self._get_property("twitter:title")

    @property
    def description(self):
        return self._get_property("twitter:description")

    @property
    def image(self):
        return self._get_property("twitter:image")
