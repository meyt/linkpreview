import time
import requests

from typing import Union

from .exceptions import (
    InvalidContentError,
    InvalidMimeTypeError,
    MaximumContentSizeError,
)
from .headers import headers_map

INITIAL_TIMEOUT = 20
MAXSIZE = 1048576
RECEIVE_TIMEOUT = 10
CHUNK_SIZE = 10


class LinkGrabber:
    headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0)"
            " Gecko/20100101"
            " Firefox/95.0"
        ),
        "accept-language": "en-US,en;q=0.5",
        "accept": (
            "text/html"
            ",application/xhtml+xml"
            ",application/xml;q=0.9"
            ",*/*;q=0.8"
        ),
    }

    def __init__(
        self,
        initial_timeout: int = INITIAL_TIMEOUT,
        maxsize: int = MAXSIZE,
        receive_timeout: int = RECEIVE_TIMEOUT,
        chunk_size: int = CHUNK_SIZE,
    ):
        """
        :param initial_timeout in seconds
        :param maxsize in bytes (default 1048576 = 1 MB)
        :param receive_timeout in seconds
        :param chunk_size in bytes
        """
        self.initial_timeout = initial_timeout
        self.maxsize = maxsize
        self.receive_timeout = receive_timeout
        self.chunk_size = chunk_size

    def get_content(
        self,
        url: str,
        headers: Union[dict, str] = None,
        replace_headers: bool = False,
    ):
        if isinstance(headers, str):
            replace_headers = True
            headers = headers_map[headers]()

        r = requests.get(
            url,
            stream=True,
            timeout=self.initial_timeout,
            headers=(
                headers
                if replace_headers
                else {**self.headers, **headers} if headers else self.headers
            ),
        )
        r.raise_for_status()

        content_type = r.headers.get("content-type")
        if not content_type:
            raise InvalidContentError("Invalid content type")

        mime_type = content_type.split(";")[0].lower()
        if mime_type != "text/html":
            raise InvalidMimeTypeError("Invalid mime type")

        length = r.headers.get("Content-Length")
        if length and int(length) > self.maxsize:
            raise MaximumContentSizeError("response too large")

        size = 0
        start = time.time()
        content = b""
        for chunk in r.iter_content(self.chunk_size):
            if time.time() - start > self.receive_timeout:
                raise TimeoutError("timeout reached")

            size += len(chunk)
            if size > self.maxsize:
                raise MaximumContentSizeError("response too large")

            content += chunk

        return content, r.url
