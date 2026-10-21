# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import csv
from pathlib import Path

import pytest
from click.testing import CliRunner

from buildingid.code import encode
from buildingid.command_line import cli


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


@pytest.mark.parametrize("left_is_larger", [True, False])
def test_crossref_matches_intersections_with_either_spatial_index(tmp_path: Path, left_is_larger: bool):
    matching_code = str(encode(0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    distant_code = str(encode(20.0, 20.0, 20.0, 20.0, 20.0, 20.0))
    matching_left = {"UBID": matching_code, "Name": "left match"}
    matching_right = {"UBID": matching_code, "Name": "right match"}
    distant_left = {"UBID": distant_code, "Name": "left distant"}
    distant_right = {"UBID": distant_code, "Name": "right distant"}

    left_rows = [matching_left, distant_left] if left_is_larger else [matching_left]
    right_rows = [matching_right] if left_is_larger else [matching_right, distant_right]
    left_path = tmp_path / "left.csv"
    right_path = tmp_path / "right.csv"
    output_path = tmp_path / "output.csv"
    write_csv(left_path, left_rows)
    write_csv(right_path, right_rows)

    result = CliRunner().invoke(
        cli,
        [
            "crossref",
            str(left_path),
            str(right_path),
            str(output_path),
            "--include-jaccard-field",
            "--include-index-fields",
            "--include-left-field",
            "Name",
            "--include-right-field",
            "Name",
        ],
    )

    assert result.exit_code == 0, result.output
    with output_path.open(encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows == [
        {
            "index_x": "0",
            "index_y": "0",
            "IoU": "1.0",
            "UBID_x": matching_code,
            "Name_x": "left match",
            "UBID_y": matching_code,
            "Name_y": "right match",
        },
    ]
