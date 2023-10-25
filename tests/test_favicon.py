from linkpreview import link_preview

from tests.helpers import get_sample


def test_favicon():
    baseurl = "http://example.com"

    # absolute favicon
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/absolute.html"),
    )
    assert preview.favicon == (
        ("http://thesite.com/favicon.ico", None, "shortcut icon"),
    )
    assert preview.absolute_favicon == (
        (preview.favicon[0][0], None, "shortcut icon"),
    )

    # relative favicon from root
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/relative.html"),
    )
    assert preview.favicon == (("/path/to/favicon.ico", None, "icon"),)
    assert preview.absolute_favicon == (
        (baseurl + preview.favicon[0][0], None, "icon"),
    )

    # relative favicon from current path
    preview = link_preview(
        url=baseurl + "/article/333/",
        content=get_sample("favicon/relative2.html"),
    )
    assert preview.favicon == (("path/to/favicon.ico", None, "icon"),)
    assert preview.absolute_favicon == (
        (baseurl + "/article/333/" + preview.favicon[0][0], None, "icon"),
    )

    preview = link_preview(
        url=baseurl + "/article/444/index.html",
        content=get_sample("favicon/relative2.html"),
    )
    assert preview.favicon == (("path/to/favicon.ico", None, "icon"),)
    assert preview.absolute_favicon == (
        (baseurl + "/article/444/" + preview.favicon[0][0], None, "icon"),
    )

    # favicon placed out of page head tag, but still valid
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/badplace.html"),
    )
    assert preview.favicon == (("/path/to/favicon.ico", None, "icon"),)

    # invalid rel attribute
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/invalid-rel.html"),
    )
    assert preview.favicon == ()

    # empty rel attribute
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/empty-rel.html"),
    )
    assert preview.favicon == ()

    # empty href attribute
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/empty-href.html"),
    )
    assert preview.favicon == ()

    # duplicate
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/duplicate.html"),
    )
    assert preview.favicon == (
        ("favicon.ico", None, "icon"),
        ("favicon.ico", None, "icon"),
    )

    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/duplicate2.html"),
    )
    assert preview.favicon == (
        ("favicon1.ico", None, "icon"),
        ("favicon2.ico", None, "icon"),
    )

    # sizes
    preview = link_preview(
        url=baseurl,
        content=get_sample("favicon/sizes.html"),
    )
    assert preview.favicon == (
        ("/apple-touch-icon.png", ((180, 180),), "apple-touch-icon"),
        ("/favicon-32x32.png", ((32, 32),), "icon"),
        ("/favicon-16x16.png", ((16, 16),), "icon"),
        ("/favicon.ico", ((32, 32), (16, 16)), "shortcut icon"),
        ("/favicon.ico", None, "icon"),
    )
    assert preview.absolute_favicon == (
        (baseurl + "/apple-touch-icon.png", ((180, 180),), "apple-touch-icon"),
        (baseurl + "/favicon-32x32.png", ((32, 32),), "icon"),
        (baseurl + "/favicon-16x16.png", ((16, 16),), "icon"),
        (baseurl + "/favicon.ico", ((32, 32), (16, 16)), "shortcut icon"),
        (baseurl + "/favicon.ico", None, "icon"),
    )
