# linkpreview

[![Build Status](https://github.com/meyt/linkpreview/actions/workflows/main.yaml/badge.svg)](https://github.com/meyt/linkpreview/actions)
[![Coverage Status](https://coveralls.io/repos/github/meyt/linkpreview/badge.svg?branch=master)](https://coveralls.io/github/meyt/linkpreview?branch=master)
[![pypi](https://img.shields.io/pypi/pyversions/linkpreview.svg)](https://pypi.python.org/pypi/linkpreview)

Get link preview in python

Gathering data from:

1. [OpenGraph](https://ogp.me/) meta tags
2. [TwitterCard](https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/abouts-cards) meta tags
3. [Microdata](https://en.wikipedia.org/wiki/Microdata_(HTML)) meta tags
4. [JSON-LD](https://en.wikipedia.org/wiki/JSON-LD) meta tags
5. HTML Generic tags (`h1`, `p`, `img`)
6. URL readable parts

## Install

```
pip install linkpreview
```

## Usage

### Basic

```python
from linkpreview import link_preview

url = "http://localhost"
content = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <!-- ... --->
    <title>a title</title>
  </head>
  <body>
  <!-- ... --->
  </body>
</html>
"""
preview = link_preview(url, content)
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
print("site_name:", preview.site_name)
print("favicon:", preview.favicon)
print("absolute_favicon:", preview.absolute_favicon)
```

### Automatic fetch link content

```python
from linkpreview import link_preview

preview = link_preview("http://github.com/")
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
print("site_name:", preview.site_name)
print("favicon:", preview.favicon)
print("absolute_favicon:", preview.absolute_favicon)
```

### `lxml` as XML parser

Very recommended for better performance.

[Install](https://lxml.de/installation.html) the `lxml` and use it like this:

```python
from linkpreview import link_preview

preview = link_preview("http://github.com/", parser="lxml")
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
print("site_name:", preview.site_name)
print("favicon:", preview.favicon)
print("absolute_favicon:", preview.absolute_favicon)
```

### Advanced

```python
from linkpreview import Link, LinkPreview, LinkGrabber

url = "http://github.com"
grabber = LinkGrabber(
    initial_timeout=20,
    maxsize=1048576,
    receive_timeout=10,
    chunk_size=1024,
)
content, url = grabber.get_content(url)
link = Link(url, content)
preview = LinkPreview(link, parser="lxml")
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
print("site_name:", preview.site_name)
print("favicon:", preview.favicon)
print("absolute_favicon:", preview.absolute_favicon)
```
