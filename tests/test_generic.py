import pytest

from linkpreview import Link
from linkpreview.preview import Generic

from tests.helpers import get_sample


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
        (
            "img-nosrc-invalid.html",
            {
                "title": None,
                "description": None,
                "image": None,
            },
        ),
        (
            "img-nosrc.html",
            {
                "title": None,
                "description": None,
                "image": "/uploads/animal/dog.png",
            },
        ),
    ),
)
def test_generic(tin, tout):
    link = Link("http://localhost", content=get_sample("generic/%s" % tin))
    preview = Generic(link, parser="html.parser")
    for key in tout.keys():
        assert getattr(preview, key) == tout[key]


@pytest.mark.parametrize(
    "tin, tout",
    (
        ("http://localhost", "localhost"),
        ("http://site.com", "site.com"),
        ("http://site.com:8080", "site.com"),
        ("http://root@site.com:8080", "site.com"),
        ("http://root:passwd@site.com:8080", "site.com"),
        ("http://root:passwd@a.b.site.com:8080", "a.b.site.com"),
        ("http://root:passwd@🍕.com:8080", "🍕.com"),
        ("http://root:passwd@xn--vi8h.com:8080", "xn--vi8h.com"),
        ("root:passwd@site.com:8080", ""),
    ),
)
def test_site_name(tin, tout):
    link = Link(tin, content="")
    preview = Generic(link, parser="html.parser")
    assert preview.site_name == tout
