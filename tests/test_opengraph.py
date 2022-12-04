import pytest

from linkpreview import Link
from linkpreview.preview import OpenGraph

from tests.helpers import get_sample


@pytest.mark.parametrize(
    "tin, tout",
    (
        (
            "available.html",
            {"title": "a title", "description": "لورم ایپزوم", "image": None},
        ),
        (
            "unavailable.html",
            {"title": None, "description": None, "image": None},
        ),
        (
            "with-image.html",
            {
                "title": "a title",
                "description": None,
                "image": "/img/heck.jpg",
            },
        ),
    ),
)
def test_opengraph(tin, tout):
    link = Link("http://localhost", content=get_sample("opengraph/%s" % tin))
    preview = OpenGraph(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]
