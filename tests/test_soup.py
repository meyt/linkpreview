import pytest
from bs4 import BeautifulSoup

from linkpreview import Link, LinkPreview

from tests.helpers import get_sample


def test_bs4_object():
    content = get_sample("generic/title.html")
    link = Link(url="http://localhost", content=content)
    bs_content = BeautifulSoup(content, "html.parser")
    preview = LinkPreview(link, soup=bs_content)
    assert preview.title == "This title is at the title tag."
    assert preview.description is None
    assert preview.image is None


def test_invalid_arguments():
    link = Link("http://localhost")
    bs_content = BeautifulSoup()
    with pytest.raises(Exception):
        LinkPreview(link, parser="html.parser", soup=bs_content)
