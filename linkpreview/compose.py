from linkpreview import Link, LinkGrabber, linkpreview
from linkpreview.exceptions import InvalidMimeTypeError


def link_preview(
    url: str = None,
    content: str = None,
    parser: str = linkpreview.PARSER,
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
    return linkpreview.LinkPreview(link, parser=parser)
