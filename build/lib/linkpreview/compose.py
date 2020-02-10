from linkpreview import Link, LinkGrabber, LinkPreview


def link_preview(
    url: str = None, content: str = None, parser: str = "html.parser"
):
    """
    Get link preview
    """
    if content is None:
        grabber = LinkGrabber()
        content = grabber.get_content(url)

    link = Link(url, content)
    return LinkPreview(link, parser=parser)
