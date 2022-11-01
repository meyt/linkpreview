import pytest

from os.path import dirname

from pytest_httpserver import HTTPServer

from werkzeug.wrappers.response import Response

from linkpreview import Link, link_preview
from linkpreview.preview import OpenGraph, TwitterCard, Schema, Generic

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
    link = Link("http://localhost", content=get_sample("open-graph/%s" % tin))
    preview = OpenGraph(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]


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
def test_twitter_card(tin, tout):
    link = Link(
        "http://localhost", content=get_sample("twitter-card/%s" % tin)
    )
    preview = TwitterCard(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]


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
def test_schema(tin, tout):
    link = Link("http://localhost", content=get_sample("schema/%s" % tin))
    preview = Schema(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]


@pytest.mark.parametrize(
    "tin, tout",
    (
        ("empty.html", {"title": None, "description": None, "image": None}),
        (
            "title.html",
            {
                "title": "This title is at the title tag.",
                "description": None,
                "image": None,
            },
        ),
        (
            "h1-title.html",
            {
                "title": "This title is from the first h1 tag.",
                "description": None,
                "image": None,
            },
        ),
        (
            "meta-desc.html",
            {
                "title": None,
                "description": "This description is meta[name='description'].",
                "image": None,
            },
        ),
        (
            "h1-p-desc.html",
            {
                "title": "This is the first heading.",
                "description": "This is valid description.",
                "image": None,
            },
        ),
        (
            "p-desc.html",
            {
                "title": None,
                "description": "This description is from the first p.",
                "image": None,
            },
        ),
        (
            "h1-img.html",
            {
                "title": "This title is from the first h1 tag.",
                "description": None,
                "image": "http://localhost:8000/img/heck.jpg",
            },
        ),
        (
            "h1-img-far.html",
            {
                "title": "This title is from the first h1 tag.",
                "description": "Some blabla content",
                "image": "http://localhost:8000/img/heck1.jpg",
            },
        ),
        (
            "h1-img-far2.html",
            {
                "title": "This title is from the first h1 tag.",
                "description": "Some blabla content",
                "image": "http://localhost:8000/img/heck.jpg",
            },
        ),
        (
            "invalid-meta.html",
            {
                "title": "INVALID PAGE",
                "description": None,
                "image": None,
            },
        ),
        (
            "invalid-meta-syntax.html",
            {
                "title": "INVALID PAGE2",
                "description": "Jack",
                "image": None,
            },
        ),
    ),
)
def test_generic(tin, tout):
    link = Link("http://localhost", content=get_sample("generic/%s" % tin))
    preview = Generic(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]


def test_link_preview(httpserver: HTTPServer):
    httpserver.expect_request("/preview1").respond_with_data(
        get_sample("twitter-card/with-image.html"),
        headers={"content-type": "text/html"},
    )
    httpserver.expect_request("/preview2").respond_with_data(
        get_sample("generic/h1-img.html"),
        headers={"content-type": "text/html"},
    )
    httpserver.expect_request("/preview-3.json").respond_with_data(
        "{}",
        headers={"content-type": "application/json"},
    )
    httpserver.expect_request("/redirected").respond_with_data(
        get_sample("generic/h1-img.html"),
        headers={"content-type": "text/html"},
    )
    redirected_url = "http://%s:%s/redirected" % (
        httpserver.host,
        httpserver.port,
    )
    httpserver.expect_request("/redirection").respond_with_response(
        Response(
            mimetype="text/html",
            headers={"location": redirected_url},
            status=301,
        )
    )

    url = httpserver.url_for("/preview1")
    preview = link_preview(url)
    assert preview.title == "a title"
    assert preview.force_title == "a title"
    assert preview.description is None
    assert preview.image == "/img/heck.jpg"
    assert preview.absolute_image == "%s%s" % (dirname(url), preview.image)

    url = httpserver.url_for("/preview2")
    preview = link_preview(url)
    assert preview.title == "This title is from the first h1 tag."
    assert preview.description is None
    assert preview.image == "http://localhost:8000/img/heck.jpg"
    assert preview.absolute_image == "http://localhost:8000/img/heck.jpg"

    preview = link_preview("https://example.com", content="OK")
    assert preview.title is None
    assert preview.description is None
    assert preview.image is None
    assert preview.absolute_image is None
    assert preview.force_title == "example.com"

    preview = link_preview("https://example.com/bird.jpg", content="OK")
    assert preview.force_title == "Bird"

    preview = link_preview("https://abc.com/the-bunny(720p).mkv", content="OK")
    assert preview.force_title == "The Bunny(720P)"

    preview = link_preview(
        "https://abc.com/the-bunny(720p)_season-1.mkv", content="OK"
    )
    assert preview.force_title == "The Bunny(720P) Season 1"

    preview = link_preview(
        "https://alex:123@abc.com/the-bunny(720p)", content="OK"
    )
    assert preview.force_title == "abc.com/the-bunny(720p)"

    preview = link_preview("https://192.168.1.1", content="OK")
    assert preview.force_title == "192.168.1.1"

    preview = link_preview("https://192.168.1.1:9696", content="OK")
    assert preview.force_title == "192.168.1.1:9696"

    preview = link_preview(httpserver.url_for("/preview-3.json"))
    assert preview.title is None
    assert preview.description is None
    assert preview.image is None
    assert preview.absolute_image is None
    assert preview.force_title == "Preview 3"

    url = httpserver.url_for("/redirection")
    preview = link_preview(url)
    assert preview.link.url == redirected_url
    assert preview.title == "This title is from the first h1 tag."
    assert preview.description is None
    assert preview.image == "http://localhost:8000/img/heck.jpg"
    assert preview.absolute_image == "http://localhost:8000/img/heck.jpg"


def test_image():
    baseurl = "http://thesite.com"

    # absolute image
    preview = link_preview(
        url=baseurl + "/article/111",
        content=get_sample("generic/img-absolute.html"),
    )
    assert preview.image == "http://thesitescdn.com/uploads/animal/dog.png"
    assert preview.absolute_image == preview.image

    # relative image from root
    preview = link_preview(
        url=baseurl + "/article/222",
        content=get_sample("generic/img-relative.html"),
    )
    assert preview.image == "/uploads/animal/dog.png"
    assert preview.absolute_image == baseurl + preview.image

    # relative image from current path
    preview = link_preview(
        url=baseurl + "/article/333/",
        content=get_sample("generic/img-relative2.html"),
    )
    assert preview.image == "animal/dog.png"
    assert preview.absolute_image == baseurl + "/article/333/" + preview.image

    preview = link_preview(
        url=baseurl + "/article/444/index.html",
        content=get_sample("generic/img-relative2.html"),
    )
    assert preview.image == "animal/dog.png"
    assert preview.absolute_image == baseurl + "/article/444/" + preview.image
