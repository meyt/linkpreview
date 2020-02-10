from urllib.parse import urlparse, urlunparse


class Link:
    """ Dynamic link (`url` (parse/unpars)ed when set/get) """

    def __init__(self, url: str, content: str = None):
        self.url = url
        self.content = content

    @property
    def url(self):
        return urlunparse(
            (
                self.scheme,
                self.netloc,
                self.path,
                self.params,
                self.query,
                self.fragment,
            )
        )

    @url.setter
    def url(self, url):
        self._url = url
        parsed_url = urlparse(url)

        self.scheme = parsed_url.scheme
        self.path = parsed_url.path
        self.query = parsed_url.query

        self.fragment = parsed_url.fragment
        self.port = parsed_url.port
        self.params = parsed_url.params

        self.netloc = parsed_url.netloc

    def copy(self):
        return Link(self._url)

    @property
    def may_file(self):
        if not self.path:
            return False

        return len(self.path.split(".")) > 1
