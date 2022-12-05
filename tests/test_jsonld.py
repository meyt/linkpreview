import pytest


from linkpreview import Link
from linkpreview.preview import JsonLd

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
                "site_name": "a title",
            },
        ),
        (
            "unavailable.html",
            {
                "title": None,
                "description": None,
                "image": None,
                "site_name": None,
            },
        ),
        (
            "with-image.html",
            {
                "title": "a title",
                "description": None,
                "image": "/img/heck.jpg",
                "site_name": None,
            },
        ),
        (
            "with-thumbnail.html",
            {
                "title": "a title",
                "description": None,
                "image": "/img/heck.jpg",
                "site_name": None,
            },
        ),
        (
            "invalid.html",
            {
                "title": None,
                "description": None,
                "image": None,
                "site_name": None,
            },
        ),
        (
            "article-website.html",
            {
                "title": "The Article",
                "description": None,
                "image": None,
                "site_name": "The Website",
            },
        ),
        (
            "website-article.html",
            {
                "title": "The Article",
                "description": None,
                "image": None,
                "site_name": "The Website",
            },
        ),
        (
            "sitename.html",
            {
                "title": "The Website",
                "description": None,
                "image": None,
                "site_name": "The Website",
            },
        ),
    ),
)
def test_jsonld(tin, tout):
    link = Link("http://localhost", content=get_sample("jsonld/%s" % tin))
    preview = JsonLd(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]
