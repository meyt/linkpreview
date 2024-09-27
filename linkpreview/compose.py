from typing import Union

from linkpreview import Link, grabber, linkpreview
from linkpreview.exceptions import InvalidMimeTypeError


def link_preview(
    url: str = None,
    content: str = None,
    parser: Union[None, str] = None,
    headers: Union[dict, str] = None,
    replace_headers: bool = False,
    initial_timeout: int = grabber.INITIAL_TIMEOUT,
    maxsize: int = grabber.MAXSIZE,
    receive_timeout: int = grabber.RECEIVE_TIMEOUT,
    chunk_size: int = grabber.CHUNK_SIZE,
):
    """
    Get link preview
    """
    if content is None:
        try:
            gb = grabber.LinkGrabber(
                initial_timeout=initial_timeout,
                maxsize=maxsize,
                receive_timeout=receive_timeout,
                chunk_size=chunk_size,
            )
            content, url = gb.get_content(
                url,
                headers=headers,
                replace_headers=replace_headers,
            )
        except InvalidMimeTypeError:
            content = ""

    link = Link(url, content)
    return linkpreview.LinkPreview(link, parser=parser)
