# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import codecs
import io
from collections.abc import Generator
from contextlib import contextmanager
from typing import TextIO


@contextmanager
def csv_text_stream(stream: TextIO) -> Generator[TextIO, None, None]:
    """Borrow a CSV-safe text view before reading from the original stream.

    Text-only streams are used unchanged. Buffered streams retain their encoding
    and error handling, except that ASCII falls back to UTF-8 as it did in Click.
    """
    buffer = getattr(stream, "buffer", None)
    if buffer is None:
        yield stream
        return

    encoding = stream.encoding or "utf-8"
    if codecs.lookup(encoding).name == "ascii":
        encoding = "utf-8"

    stream.flush()
    wrapper = io.TextIOWrapper(
        buffer,
        encoding=encoding,
        errors=stream.errors or "strict",
        newline="",
        line_buffering=getattr(stream, "line_buffering", False),
        write_through=getattr(stream, "write_through", False),
    )
    try:
        yield wrapper
    finally:
        wrapper.detach()
