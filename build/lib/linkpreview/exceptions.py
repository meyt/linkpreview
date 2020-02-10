class LinkPreviewException(Exception):
    pass


class InvalidContentError(LinkPreviewException):
    pass


class InvalidMimeTypeError(InvalidContentError):
    pass


class MaximumContentSizeError(InvalidContentError):
    pass
