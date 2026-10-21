# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import csv
import io

import pytest

from buildingid.command_line.csv_stream import csv_text_stream


def test_csv_text_stream_preserves_embedded_newlines():
    data = b'Name,Value\r\n"first\r\nsecond",1\r\n'
    with io.TextIOWrapper(io.BytesIO(data), encoding="utf-8", newline=None) as original:
        with csv_text_stream(original) as stream:
            assert list(csv.reader(stream)) == [["Name", "Value"], ["first\r\nsecond", "1"]]

        assert not original.closed
        assert original.encoding == "utf-8"


@pytest.mark.parametrize(
    ("encoding", "expected_encoding"),
    [("utf-8", "utf-8"), ("ascii", "utf-8"), ("us-ascii", "utf-8"), ("latin-1", "latin-1")],
)
def test_csv_text_stream_respects_encoding_without_windows_translation(encoding: str, expected_encoding: str):
    with io.TextIOWrapper(io.BytesIO(), encoding=encoding, newline="\r\n") as original:
        original.write("prefix\n")
        with csv_text_stream(original) as stream:
            csv.writer(stream).writerow(["caf\u00e9\r\nannex", "1"])

        assert not original.closed
        original.write("suffix\n")
        original.flush()
        assert original.buffer.getvalue() == 'prefix\r\n"caf\u00e9\r\nannex",1\r\nsuffix\r\n'.encode(expected_encoding)


def test_csv_text_stream_preserves_error_handling():
    with io.TextIOWrapper(io.BytesIO(), encoding="utf-8", errors="surrogateescape") as original:
        with csv_text_stream(original) as stream:
            stream.write("\udcff")

        assert original.buffer.getvalue() == b"\xff"
        assert original.errors == "surrogateescape"


def test_csv_text_stream_leaves_original_open_after_exception():
    with io.TextIOWrapper(io.BytesIO(), encoding="utf-8", newline="\r\n") as original:

        def write_and_fail():
            with csv_text_stream(original) as stream:
                stream.write("row\r\n")
                raise RuntimeError("test failure")

        with pytest.raises(RuntimeError, match="test failure"):
            write_and_fail()

        assert not original.closed
        assert original.buffer.getvalue() == b"row\r\n"


def test_csv_text_stream_uses_text_only_stream_unchanged():
    with io.StringIO() as original:
        with csv_text_stream(original) as stream:
            assert stream is original
            csv.writer(stream).writerow(["value"])

        assert not original.closed
        assert original.getvalue() == "value\r\n"
