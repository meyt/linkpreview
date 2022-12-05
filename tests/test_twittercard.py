import pytest

from linkpreview import Link
from linkpreview.preview import TwitterCard

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
                "site_name": None,
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
    ),
)
def test_twitter_card(tin, tout):
    link = Link("http://localhost", content=get_sample("twittercard/%s" % tin))
    preview = TwitterCard(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]
