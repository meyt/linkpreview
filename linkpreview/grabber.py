import ipaddress
import socket
import time
from typing import Union
from urllib.parse import urljoin, urlsplit

import requests

from .exceptions import (
    BlockedAddressError,
    InvalidContentError,
    InvalidMimeTypeError,
    MaximumContentSizeError,
)
from .headers import headers_map

INITIAL_TIMEOUT = 20
MAXSIZE = 1048576
RECEIVE_TIMEOUT = 10
CHUNK_SIZE = 10
MAX_REDIRECTS = 30


class LinkGrabber:
    headers = {
        "user-agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0)"
            " Gecko/20100101"
            " Firefox/95.0"
        ),
        "accept-language": "en-US,en;q=0.5",
        "accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        ),
    }

    def __init__(
        self,
        initial_timeout: int = INITIAL_TIMEOUT,
        maxsize: int = MAXSIZE,
        receive_timeout: int = RECEIVE_TIMEOUT,
        chunk_size: int = CHUNK_SIZE,
        allow_private: bool = True,
        max_redirects: int = MAX_REDIRECTS,
    ):
        """
        :param initial_timeout in seconds
        :param maxsize in bytes (default 1048576 = 1 MB)
        :param receive_timeout in seconds
        :param chunk_size in bytes
        :param max_redirects number of redirects to follow
        :param allow_private set False for untrusted URLs: only http(s) to
            public addresses is fetched, checked again on every redirect
        """
        self.initial_timeout = initial_timeout
        self.maxsize = maxsize
        self.receive_timeout = receive_timeout
        self.chunk_size = chunk_size
        self.allow_private = allow_private
        self.max_redirects = max_redirects

    def _check_url(self, url: str):
        parts = urlsplit(url)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise BlockedAddressError("Blocked url scheme")
        # shortcut: resolves before requests resolves again, so DNS rebinding
        # can still slip through; pin the IP in an HTTPAdapter to close it
        for *_, addr in socket.getaddrinfo(parts.hostname, parts.port):
            ip = ipaddress.ip_address(addr[0].split("%")[0])
            if not ip.is_global:
                raise BlockedAddressError("Blocked address")

    def get_content(
        self,
        url: str,
        headers: Union[dict, str] = None,
        replace_headers: bool = False,
    ):
        if isinstance(headers, str):
            replace_headers = True
            headers = headers_map[headers]()

        headers = (
            headers
            if replace_headers
            else {**self.headers, **headers}
            if headers
            else self.headers
        )
        for _ in range(self.max_redirects + 1):
            if not self.allow_private:
                self._check_url(url)
            r = requests.get(
                url,
                stream=True,
                timeout=self.initial_timeout,
                headers=headers,
                allow_redirects=False,
            )
            if not r.is_redirect:
                break
            url = urljoin(url, r.headers["location"])
            r.close()
        else:
            raise requests.TooManyRedirects("Too many redirects")
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
