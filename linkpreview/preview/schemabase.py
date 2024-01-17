from linkpreview.preview.base import PreviewBase
from linkpreview.helpers import LazyAttribute

WEBSITE = "website"
ORGANIZATION = "organization"
BLOG = "blog"
site_types = (WEBSITE, BLOG, ORGANIZATION)


class SchemaPreviewBase(PreviewBase):
    """
    Schema.org meta properties
    """

    schema_netloc = "schema.org"

    def get_schema(self):  # pragma:nocover
        raise NotImplementedError

    @LazyAttribute
    def schema(self):
        return tuple(self.get_schema())

    @LazyAttribute
    def sorted_schema(self):
        return sorted(self.schema, key=lambda x: x["type"] in site_types)

    @property
    def site_name(self):
        for item in self.schema:
            if item["type"] not in site_types:
                continue

            if "name" in item:
                return item["name"]

    @property
    def title(self):
        for item in self.sorted_schema:
            if "name" in item:
                return item["name"]

    @property
    def description(self):
        for item in self.sorted_schema:
            if "description" in item:
                return item["description"]

    @staticmethod
    def _extract_image(v):
        # https://schema.org/image
        # https://schema.org/ImageObject
        if isinstance(v, str):
            return v

        if isinstance(v, dict) and 'url' in v:
            url = v['url']
            if isinstance(url, str) and len(url):
                return url

    @property
    def image(self):
        for item in self.sorted_schema:
            if "image" in item:
                return self._extract_image(item["image"])

            if "thumbnailUrl" in item:
                return self._extract_image(item["thumbnailUrl"])
