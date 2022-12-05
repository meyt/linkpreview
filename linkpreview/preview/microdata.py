from urllib.parse import urlparse

from linkpreview.preview.schemabase import SchemaPreviewBase


class Microdata(SchemaPreviewBase):
    """
    sample:
    <div itemscope itemtype="https://schema.org/Article">
        <div itemprop="name" content="blabla"></div>
    </div>
    """

    def get_schema(self):
        for scope in self._soup.find_all(attrs={"itemscope": True}):
            if not scope.has_attr("itemtype"):
                continue

            for type_ in scope["itemtype"].split(" "):

                # Validate the type URL
                typeurl = urlparse(type_)
                if (
                    not typeurl.path
                    or typeurl.netloc.lower() != self.__class__.schema_netloc
                ):
                    continue

                # Use the type URL's path as identifier
                type_ = typeurl.path.lower().strip("/")
                item = dict(type=type_)
                for itemprop in scope.find_all(attrs={"itemprop": True}):
                    if not itemprop.has_attr("content"):
                        continue

                    item[itemprop["itemprop"]] = itemprop["content"]

                yield item
