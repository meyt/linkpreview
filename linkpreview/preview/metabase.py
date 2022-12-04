from linkpreview.preview.base import PreviewBase


class MetaPreviewBase(PreviewBase):
    """
    Abstract class for OpenGraph, TwitterCard and Microdata.
    """

    __target_attr__ = None

    def _get_property(self, name):
        meta = self._soup.find("meta", attrs={self.__target_attr__: name})
        if meta and meta["content"]:
            return meta["content"]
