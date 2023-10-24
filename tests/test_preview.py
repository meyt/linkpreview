from os.path import dirname

from pytest_httpserver import HTTPServer

from werkzeug.wrappers.response import Response

from linkpreview import link_preview

from tests.helpers import get_sample


def test_link_preview(httpserver: HTTPServer):
    httpserver.expect_request("/preview1").respond_with_data(
        get_sample("twittercard/with-image.html"),
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
    assert preview.site_name == "localhost"

    url = httpserver.url_for("/preview2")
    preview = link_preview(url)
    assert preview.title == "This title is from the first h1 tag."
    assert preview.description is None
    assert preview.image == "http://localhost:8000/img/heck.jpg"
    assert preview.absolute_image == "http://localhost:8000/img/heck.jpg"
    assert preview.site_name == "localhost"

    preview = link_preview("https://example.com", content="OK")
    assert preview.title is None
    assert preview.description is None
    assert preview.image is None
    assert preview.absolute_image is None
    assert preview.force_title == "example.com"
    assert preview.site_name == "example.com"

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
    assert preview.site_name == "abc.com"

    preview = link_preview("https://192.168.1.1", content="OK")
    assert preview.force_title == "192.168.1.1"
    assert preview.site_name == "192.168.1.1"

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
    assert preview.to_dict() == {
        "site_name": "localhost",
        "title": "This title is from the first h1 tag.",
        "description": None,
        "image": "http://localhost:8000/img/heck.jpg",
        "absolute_image": "http://localhost:8000/img/heck.jpg",
        "force_title": "This title is from the first h1 tag.",
        "favicon": (),
        "absolute_favicon": (),
    }


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
