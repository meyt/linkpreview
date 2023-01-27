import pytest

from time import sleep

from pytest_httpserver import HTTPServer

from werkzeug.wrappers.response import Response

from requests.exceptions import ReadTimeout

from linkpreview import LinkGrabber
from linkpreview import exceptions

from tests.helpers import get_sample


def test_grabber(httpserver: HTTPServer):

    sample = get_sample("generic/h1-p-desc.html")

    class FakeResponse(Response):
        automatically_set_content_length = False

    httpserver.expect_request("/h1-p-desc").respond_with_data(
        sample, headers={"content-type": "text/html"}
    )
    httpserver.expect_request("/lazy").respond_with_handler(
        lambda x: sleep(0.6)
    )
    httpserver.expect_request("/huge").respond_with_response(
        FakeResponse(
            response=b"x" * 100000,
            mimetype="text/html",
        )
    )
    httpserver.expect_request("/badmime").respond_with_data(
        "{}", headers={"content-type": "application/json"}
    )
    httpserver.expect_request("/nomime").respond_with_response(
        Response(mimetype="")
    )
    httpserver.expect_request("/large").respond_with_response(
        FakeResponse(
            mimetype="text/html",
            headers={"content-length": "100000"},
        )
    )
    httpserver.expect_request("/redirected").respond_with_response(
        FakeResponse(
            mimetype="text/html",
            response=b"done!",
        )
    )
    redirected_url = "http://%s:%s/redirected" % (
        httpserver.host,
        httpserver.port,
    )
    httpserver.expect_request("/redirection").respond_with_response(
        FakeResponse(
            mimetype="text/html",
            headers={"location": redirected_url},
            status=301,
        )
    )
    httpserver.expect_request("/headers").respond_with_handler(
        lambda x: FakeResponse(
            response=x.headers["user-agent"].encode(),
            mimetype="text/html",
        )
    )

    # success
    grabber = LinkGrabber(maxsize=100)
    with pytest.raises(exceptions.MaximumContentSizeError):
        grabber.get_content(httpserver.url_for("/h1-p-desc"))

    # initial timeout
    grabber = LinkGrabber(initial_timeout=0.5)
    with pytest.raises(ReadTimeout):
        grabber.get_content(httpserver.url_for("/lazy"))

    # receive timeout
    grabber = LinkGrabber(receive_timeout=0.1, chunk_size=1)
    with pytest.raises(TimeoutError):
        grabber.get_content(httpserver.url_for("/huge"))

    # maxsize
    grabber = LinkGrabber(receive_timeout=10000, chunk_size=1024, maxsize=20)
    with pytest.raises(exceptions.MaximumContentSizeError):
        grabber.get_content(httpserver.url_for("/huge"))

    # large
    grabber = LinkGrabber(maxsize=100)
    with pytest.raises(exceptions.MaximumContentSizeError):
        grabber.get_content(httpserver.url_for("/large"))

    # nomime
    grabber = LinkGrabber()
    with pytest.raises(exceptions.InvalidContentError):
        grabber.get_content(httpserver.url_for("/nomime"))

    # badmime
    grabber = LinkGrabber()
    with pytest.raises(exceptions.InvalidContentError):
        grabber.get_content(httpserver.url_for("/badmime"))

    # redirection
    grabber = LinkGrabber()
    content, url = grabber.get_content(httpserver.url_for("/redirection"))
    assert url == redirected_url

    # default headers
    grabber = LinkGrabber()
    content, url = grabber.get_content(httpserver.url_for("/headers"))
    assert "Mozilla/5.0" in content.decode()

    # custom headers
    grabber = LinkGrabber()
    content, url = grabber.get_content(
        httpserver.url_for("/headers"),
        headers={"user-agent": "Googlebot"},
    )
    assert "Mozilla/5.0" not in content.decode()
    assert "Googlebot" in content.decode()
