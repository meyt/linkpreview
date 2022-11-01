from linkpreview import Link, LinkGrabber, LinkPreview
from linkpreview.exceptions import InvalidMimeTypeError


def link_preview(
    url: str = None,
    content: str = None,
    parser: str = "html.parser",
):
    """
    Get link preview
    """
    if content is None:
        try:
            grabber = LinkGrabber()
            content, url = grabber.get_content(url)
        except InvalidMimeTypeError:
            content = ""

    link = Link(url, content)
    return LinkPreview(link, parser=parser)
