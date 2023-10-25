import re

from linkpreview.preview.base import PreviewBase


favicon_attr_pattern = re.compile(
    "^(shortcut icon|icon|apple-touch-icon|apple-touch-icon-precomposed)$",
    re.I,
)


class Generic(PreviewBase):
    """
    Extracts site_name, title, description, image from a webpage's body
    """

    @property
    def site_name(self):
        """
        Extract site name from URL
        """
        return self.link.netloc.split("@")[-1].split(":")[0]

    @property
    def title(self):
        """
        Extract title from the given web page.
        """
        soup = self._soup
        if soup.title and soup.title.text:
            return soup.title.text

        if soup.h1 and soup.h1.text:
            return soup.h1.text

    @property
    def description(self):
        """
        Extract description from the given web page.
        """
        soup = self._soup
        # meta[name='description']
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.has_attr("content"):
            return meta["content"]

        # else extract preview from the first <p> sibling to the first <h1>
        first_h1 = soup.find("h1")
        if first_h1:
            first_p = first_h1.find_next("p")
            if first_p and first_p.string:
                return first_p.text

        # else extract preview from the first <p>
        first_p = soup.find("p")
        if first_p and first_p.string:
            return first_p.string

    @property
    def image(self):
        """
        Extract preview image from the given web page.
        """
        soup = self._soup
        h1 = soup.find("h1")
        if h1:
            # extract the first image which is sibling to the first h1
            img = h1.find_next_sibling("img", {"src": True}) or h1.find_next(
                "img", {"src": True}
            )

        else:
            # just find something
            img = soup.find("img", {"src": True})

        if img and img["src"]:
            return img["src"]

    @staticmethod
    def _export_favicon_sizes(sizes):
        # https://developer.mozilla.org/en-US/docs/Web/HTML/Element/link#sizes
        if not sizes:
            return

        sizes = sizes.lower().strip()
        if sizes == "any":
            return

        return tuple(
            map(
                lambda x: tuple(map(int, x.split("x"))),
                sizes.split(" "),
            )
        )

    @property
    def favicon(self):
        soup = self._soup
        for item in soup.find_all("link", attrs={"rel": favicon_attr_pattern}):
            icon = item.get("href")
            if icon:
                yield (
                    icon,
                    self._export_favicon_sizes(item.get("sizes")),
                    " ".join(item.get("rel")),
                )
