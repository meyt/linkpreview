# linkpreview

[![Build Status](
    https://www.travis-ci.com/meyt/linkpreview.svg?branch=master
)](
    https://www.travis-ci.com/meyt/linkpreview
)
[![Coverage Status](
    https://coveralls.io/repos/github/meyt/linkpreview/badge.svg?branch=master
)](
    https://coveralls.io/github/meyt/linkpreview?branch=master
)
[![pypi](
    https://img.shields.io/pypi/pyversions/linkpreview.svg
)](
    https://pypi.python.org/pypi/linkpreview
)

Get link preview in python

Gathering data from:

1. [OpenGraph](https://ogp.me/) meta tags
2. [TwitterCard](https://developer.twitter.com/en/docs/tweets/optimize-with-cards/overview/abouts-cards) meta tags
3. [Schema.org](https://schema.org/) meta tags
4. HTML Generic tags (`h1`, `p`, `img`)
5. URL readable parts


## Install

```
pip install linkpreview
```

## Usage

### Basic:

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
```

### Use `lxml` as XML parser:

Very recommended for better performance

```python
from linkpreview import link_preview

preview = link_preview("http://github.com/", parser="lxml")
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
```

### Advanced

```python
from linkpreview import Link, LinkPreview, LinkGrabber

url = "http://github.com"
grabber = LinkGrabber(
    initial_timeout=20, maxsize=1048576, receive_timeout=10, chunk_size=1024,
)
content = grabber.get_content(url)
link = Link(url, content)
preview = LinkPreview(link, parser="lxml")
print("title:", preview.title)
print("description:", preview.description)
print("image:", preview.image)
print("force_title:", preview.force_title)
print("absolute_image:", preview.absolute_image)
```
