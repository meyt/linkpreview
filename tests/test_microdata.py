import pytest


from linkpreview import Link
from linkpreview.preview import Microdata

from tests.helpers import get_sample


@pytest.mark.parametrize(
    "tin, tout",
    (
        (
            "available.html",
            {
                "title": "a title",
                "description": "لورم ایپزوم",
                "image": None,
            },
        ),
        (
            "unavailable.html",
            {
                "title": None,
                "description": None,
                "image": None,
            },
        ),
        (
            "with-image.html",
            {
                "title": "a title",
                "description": None,
                "image": "/img/heck.jpg",
            },
        ),
        (
            "with-thumbnail.html",
            {
                "title": "a title",
                "description": None,
                "image": "/img/heck.jpg",
            },
        ),
        (
            "invalid.html",
            {
                "title": None,
                "description": None,
                "image": None,
            },
        ),
        (
            "article-website.html",
            {
                "title": "The Article",
                "description": None,
                "image": None,
            },
        ),
        (
            "website-article.html",
            {
                "title": "The Article",
                "description": None,
                "image": None,
            },
        ),
    ),
)
def test_microdata(tin, tout):
    link = Link("http://localhost", content=get_sample("microdata/%s" % tin))
    preview = Microdata(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]
