# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import io
import os
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from buildingid.command_line import cli

CODE = "6FG22222+22-0-0-0-0"


def run_cli(args: list[str], input_data: bytes = b"", *, io_encoding: str = "utf-8:strict") -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(  # noqa: S603 -- All arguments are controlled by these tests.
        [sys.executable, "-c", "from buildingid.command_line import cli; cli()", *args],
        input=input_data,
        capture_output=True,
        check=False,
        timeout=30,
        env={
            **os.environ,
            "PYTHONUTF8": "1",
            "PYTHONIOENCODING": io_encoding,
            "TQDM_DISABLE": "1",
        },
    )


@pytest.mark.parametrize("io_encoding", ["utf-8:strict", "ascii:strict", "latin-1:strict"])
def test_append2csv_standard_stream_bytes(io_encoding: str):
    encoding = "latin-1" if io_encoding == "latin-1:strict" else "utf-8"
    name = "caf\u00e9\r\nannex"
    input_data = f'Name,Latitude,Longitude\r\n"{name}",0,0\r\n"{name}",bad,0\r\n'.encode(encoding)

    result = run_cli(["append2csv", "latlng", "--code-length=10"], input_data, io_encoding=io_encoding)

    assert result.returncode == 0, result.stderr
    assert result.stdout == f'Name,Latitude,Longitude,UBID\r\n"{name}",0,0,{CODE}\r\n'.encode(encoding)
    assert result.stderr == (
        "Name,Latitude,Longitude,UBID_Error_Name,UBID_Error_Message\r\n"
        f"\"{name}\",bad,0,ValueError,could not convert string to float: 'bad'\r\n"
    ).encode(encoding)


@pytest.mark.parametrize("io_encoding", ["utf-8:strict", "ascii:strict"])
@pytest.mark.parametrize("stdin_side", ["left", "right", "neither"])
@pytest.mark.parametrize("use_stdout", [True, False])
def test_crossref_file_and_standard_stream_bytes(tmp_path: Path, io_encoding: str, stdin_side: str, use_stdout: bool):
    left_name = "caf\u00e9\r\nannex"
    right_name = "th\u00e9\r\nshed"
    left_data = f'UBID,Name\r\n{CODE},"{left_name}"\r\n'.encode()
    right_data = f'UBID,Name\r\n{CODE},"{right_name}"\r\n'.encode()
    left_path = tmp_path / "left.csv"
    right_path = tmp_path / "right.csv"
    output_path = tmp_path / "output.csv"
    left_path.write_bytes(left_data)
    right_path.write_bytes(right_data)
    input_data = {"left": left_data, "right": right_data, "neither": b""}[stdin_side]

    result = run_cli(
        [
            "crossref",
            "-" if stdin_side == "left" else str(left_path),
            "-" if stdin_side == "right" else str(right_path),
            "-" if use_stdout else str(output_path),
            "--include-left-field=Name",
            "--include-right-field=Name",
        ],
        input_data,
        io_encoding=io_encoding,
    )

    assert result.returncode == 0, result.stderr
    output_data = result.stdout if use_stdout else output_path.read_bytes()
    expected = f'UBID_x,Name_x,UBID_y,Name_y{os.linesep}{CODE},"{left_name}",{CODE},"{right_name}"{os.linesep}'
    assert output_data == expected.encode()
    if not use_stdout:
        assert result.stdout == b""
    assert left_path.read_bytes() == left_data
    assert right_path.read_bytes() == right_data


def test_append2csv_uses_click_runner_streams():
    result = CliRunner().invoke(cli, ["append2csv", "latlng", "--code-length=10"], input=b"Latitude,Longitude\r\n0,0\r\n")

    assert result.exit_code == 0, result.output
    assert result.stdout_bytes == f"Latitude,Longitude,UBID\r\n0,0,{CODE}\r\n".encode()
    assert result.stderr_bytes == b""


def test_append2csv_uses_redirected_text_only_streams(monkeypatch: pytest.MonkeyPatch):
    stdin = io.StringIO("Latitude,Longitude\r\n0,0\r\n")
    stdout = io.StringIO()
    stderr = io.StringIO()
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)
    monkeypatch.setattr(sys, "stderr", stderr)

    cli.main(["append2csv", "latlng", "--code-length=10"], standalone_mode=False)

    assert stdout.getvalue() == f"Latitude,Longitude,UBID\r\n0,0,{CODE}\r\n"
    assert stderr.getvalue() == ""
    assert not stdin.closed
    assert not stdout.closed
    assert not stderr.closed


def test_crossref_uses_redirected_text_only_streams(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    right_path = tmp_path / "right.csv"
    right_path.write_bytes(f"UBID\r\n{CODE}\r\n".encode())
    stdin = io.StringIO(f"UBID\r\n{CODE}\r\n")
    stdout = io.StringIO()
    monkeypatch.setattr(sys, "stdin", stdin)
    monkeypatch.setattr(sys, "stdout", stdout)

    cli.main(["crossref", "-", str(right_path), "-"], standalone_mode=False)

    assert stdout.getvalue() == f"UBID_x,UBID_y{os.linesep}{CODE},{CODE}{os.linesep}"
    assert not stdin.closed
    assert not stdout.closed


def test_append2csv_reports_invalid_encoding():
    result = run_cli(["append2csv", "latlng"], b"Name,Latitude,Longitude\r\n\xff,0,0\r\n")

    assert result.returncode != 0
    assert result.stdout == b""
    assert b"Error:" in result.stderr
    assert b"decode" in result.stderr
    assert b"Traceback" not in result.stderr
