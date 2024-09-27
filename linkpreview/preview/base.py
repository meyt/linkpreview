from typing import Union

from bs4 import BeautifulSoup
from linkpreview.link import Link


class PreviewBase(object):  # pragma: nocover
    """
    Base for all web preview.
    """

    def __init__(
        self,
        link: Link,
        parser: Union[str, None] = None,
        soup: Union[BeautifulSoup, None] = None,
    ):
        if parser and soup:
            raise Exception(
                "Only one of `parser` or `soup` argument must be provided"
            )

        if soup is None and parser is None:
            parser = "html.parser"

        self.link = link
        self._soup = soup or BeautifulSoup(self.link.content, parser)

    @property
    def title(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError

    @property
    def image(self):
        raise NotImplementedError
