try:
    import orjson as json
except ModuleNotFoundError:  # pragma: nocover
    try:
        import ujson as json
    except ModuleNotFoundError:  # pragma: nocover
        import json

from linkpreview.preview.schemabase import SchemaPreviewBase


class JsonLd(SchemaPreviewBase):
    """
    sample:
    <script type="application/ld+json">
    {
      "@context" : "https://schema.org",
      "@type" : "WebSite",
      "name" : "The Website",
      "url" : "https://example.com/"
    }
    </script>
    """

    jsonlib = json

    def get_schema(self):
        for el in self._soup.find_all(attrs=dict(type="application/ld+json")):
            jsonld = self.jsonlib.loads("".join(el.contents))

            if isinstance(jsonld, dict):
                jsonld = (jsonld,)

            for scope in jsonld:
                if "@type" not in scope:
                    continue

                item = dict(type=scope["@type"].lower())
                item.update(scope)
                yield item
