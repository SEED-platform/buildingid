# Unique Building Identifier (UBID)

[![Build Status](https://github.com/SEED-platform/buildingid/actions/workflows/test.yml/badge.svg)](https://github.com/SEED-platform/buildingid/actions/workflows/test.yml)

**Website:** <https://www.pnnl.gov/unique-building-identification>

## Documentation

### Install

To complete this guide, [Git](https://git-scm.com/) and [uv](https://docs.astral.sh/uv/getting-started/installation/) are required.
The repository's `.python-version` selects the default development interpreter.

Clone the repository, and then install the `buildingid` package:

```bash
git clone https://github.com/SEED-platform/buildingid.git
cd buildingid
uv sync
```

`uv sync` installs the package, its dependencies, and the development tools into the project's virtual environment.
Run the following commands from the repository directory using `uv run` to use that environment.

### Test

Test the `buildingid` package using the [pytest](https://docs.pytest.org/) package:

```bash
uv run pytest tests/
```

The [pytest-cov](https://pytest-cov.readthedocs.io/) plugin is installed by `uv sync`.
Coverage reporting is enabled by default in `pyproject.toml`, with an HTML report written to `htmlcov/index.html`.

### Usage

The `buildingid` package supports two usages:

- Application programming interface (API)
- Command-line interface (CLI; the `buildingid` command)

#### The API

- `buildingid.code`
  - `Code`
  - `CodeArea`
    - `area: float` (property)
    - `encode() -> Code`
    - `intersection(other: CodeArea | None) -> tuple[float, float, float, float] | None`
    - `jaccard(other: CodeArea | None) -> float | None`
    - `resize() -> CodeArea`
  - `decode(code: Code | str | None) -> CodeArea`
  - `encode(latitudeLo: float, longitudeLo: float, latitudeHi: float, longitudeHi: float, latitudeCenter: float, longitudeCenter: float, codeLength: int = 10) -> Code`
  - `isValid(code: Code | str | None) -> bool`

`Code` is a `str`-based type representing a UBID.

In the following example, a UBID code is decoded and then re-encoded:

Save the example as `example.py` and run it with `uv run python example.py`.

```python
#!/usr/bin/env python3

import buildingid.code

if __name__ == "__main__":
    # Initialize UBID code.
    orig_code = "849VQJH6+95J-51-58-42-50"
    print(orig_code)

    # Decode UBID code.
    orig_code_area = buildingid.code.decode(orig_code)
    print(orig_code_area)

    # Inset each edge by half the corresponding OLC cell dimension.
    # This changes the bounds but preserves the UBID when re-encoded.
    new_code_area = orig_code_area.resize()
    print(new_code_area)

    # Encode new UBID code area.
    new_code = new_code_area.encode()
    print(new_code)

    # Test that the re-encoded UBID matches the original.
    assert orig_code == new_code
```

#### The CLI

View the documentation for the `buildingid` command using the `--help` command-line option:

```bash
uv run buildingid --help
#=> Usage: buildingid [OPTIONS] COMMAND [ARGS]...
#=> <<more lines of output>>
```

View the documentation for a sub-command of the `buildingid` command using the `--help` command-line option.
For example, to view the documentation for the "append2csv" sub-command:

```bash
uv run buildingid append2csv --help
#=> Usage: buildingid [OPTIONS] COMMAND [ARGS]...
#=> <<more lines of output>>
```

##### Commands

| Command name | Description                                                                |
| ------------ | -------------------------------------------------------------------------- |
| append2csv   | Read CSV file from stdin, append UBID field, and write CSV file to stdout. |
| crossref     | Read two CSV files, cross-reference UBID fields, and write CSV file.       |

## Tutorials

Instructions in this section use [Bash](https://www.gnu.org/software/bash/) syntax.

### Append UBID field to CSV file

#### Prerequisites

1. `buildingid` is installed in the project environment (see [Install](#install)).
   - Verify installation:
     - `uv run buildingid --version`
       - Expected output: `buildingid, version <installed version>`

#### Step-by-step instructions

1. Locate input CSV file, e.g., `path/to/in.csv`.
2. Locate output CSV file (generated), e.g., `path/to/out.csv`.
3. Locate errors CSV file (generated), e.g., `path/to/err.csv`.
4. Identify number of digits in [Open Location Code (OLC)](https://plus.codes/) part of UBID code string, e.g., 11.
5. Identify column of output CSV file that contains UBID code strings, e.g., "UBID".
6. If input CSV file contains latitude and longitude coordinates for a centroid only:
   1. Identify columns of input CSV file that contain latitude and longitude coordinates, e.g., "Latitude" and "Longitude".
   2. Assign UBIDs:
      - `uv run buildingid append2csv latlng --code-length=11 --fieldname-code="UBID" --fieldname-center-latitude="Latitude" --fieldname-center-longitude="Longitude" < path/to/in.csv > path/to/out.csv 2> path/to/err.csv`
7. If input CSV file contains latitude and longitude coordinates for (i) a centroid and (ii) the northeast and southwest corners of a bounding box:
   1. Identify columns of input CSV file that contain latitude and longitude coordinates, e.g., "Latitude_C", "Longitude_C", "Latitude_N", "Longitude_E", "Latitude_S", and "Longitude_W".
   2. Assign UBIDs:
      - `uv run buildingid append2csv latlng --code-length=11 --fieldname-code="UBID" --fieldname-center-latitude="Latitude_C" --fieldname-center-longitude="Longitude_C" --fieldname-north-latitude="Latitude_N" --fieldname-east-longitude="Longitude_E" --fieldname-south-latitude="Latitude_S" --fieldname-west-longitude="Longitude_W" < path/to/in.csv > path/to/out.csv 2> path/to/err.csv`
8. If input CSV file contains hex-encoded [well-known binary (WKB)](https://www.iso.org/standard/60343.html) strings:
   1. Identify column of input CSV file that contains hex-encoded WKB strings, e.g., "WKB".
   2. Assign UBIDs:
      - `uv run buildingid append2csv wkb --code-length=11 --fieldname-code="UBID" --fieldname-wkbstr="WKB" < path/to/in.csv > path/to/out.csv 2> path/to/err.csv`
9. If input CSV file contains [well-known text (WKT)](https://www.iso.org/standard/60343.html) strings:
   1. Identify column of input CSV file that contains WKT strings, e.g., "WKT".
   2. Assign UBIDs:
      - `uv run buildingid append2csv wkt --code-length=11 --fieldname-code="UBID" --fieldname-wktstr="WKT" < path/to/in.csv > path/to/out.csv 2> path/to/err.csv`

#### Notes

See `uv run buildingid append2csv --help` for full help.

### Cross-reference UBID fields in two CSV files

#### Prerequisites

1. `buildingid` is installed in the project environment (see [Install](#install)).
   - Verify installation:
     - `uv run buildingid --version`
       - Expected output: `buildingid, version <installed version>`

#### Step-by-step instructions

1. Locate left input CSV file, e.g., `path/to/left.csv`.
2. Locate right input CSV file, e.g., `path/to/right.csv`.
3. Locate output CSV file (generated), e.g., `path/to/out.csv`.
4. Identify column of left input CSV file that contains UBID code strings, e.g., "UBID".
5. Identify column of right input CSV file that contains UBID code strings, e.g., "UBID".
6. Cross-reference UBIDs:
   - `uv run buildingid crossref path/to/left.csv path/to/right.csv path/to/out.csv --left-fieldname-code="UBID" --right-fieldname-code="UBID"`

#### Notes

See `uv run buildingid crossref --help` for full help.

Default behavior is for output CSV file to be many-to-many (i.e., many records in left input CSV file are cross-referenced with many records in right input CSV file).
Use `--left-group-by-jaccard` for many-to-one matching (at most one right match per left row), or `--right-group-by-jaccard` for one-to-many matching (at most one left match per right row).

Grouping selects the lowest Jaccard similarity by default (`ASC`).
Use `--left-group-order=DESC` or `--right-group-order=DESC`, respectively, to select the highest-similarity match in each group.

Default behavior is for output CSV file to include only columns that contain UBID code strings.
Use `--include-left-field` and `--include-right-field` options to include other columns.

### Convert from Esri shapefile to CSV file

#### Prerequisites

1. [Geospatial Data Abstraction Library (GDAL)](https://gdal.org/en/stable/) is installed.
   - Verify installation:
     - `ogr2ogr --version`
       - Expected output starts with `GDAL` followed by the installed version.

#### Step-by-step instructions

1. Locate input Esri shapefile, e.g., `path/to/in.shp`.
2. Locate input PRJ file, e.g., `path/to/in.prj`.
3. Locate output CSV file (generated), e.g., `path/to/out.csv`.
4. Convert input Esri shapefile into output CSV file:
   - `ogr2ogr -s_srs "$(cat path/to/in.prj)" -t_srs "EPSG:4326" -f CSV path/to/out.csv path/to/in.shp -lco GEOMETRY=AS_WKT`

#### Notes

See `ogr2ogr --long-usage` for full help.

Output CSV file has added "WKT" column whose elements are [well-known text (WKT)](https://www.iso.org/standard/60343.html) strings; enabled by `-lco GEOMETRY=AS_WKT` option.

Projection system for geographic coordinates in output CSV file is [WGS84](https://epsg.io/4326); enabled by `-t_srs "EPSG:4326"` option.

Records in input Esri shapefile are converted into rows in output CSV file, where fields in input Esri shapefile are converted into columns in output CSV file.

Shapes in input Esri shapefile are converted into elements of "WKT" column of output CSV file.

## Case Studies

### Chicago, IL

[The City of Chicago's open data portal](https://data.cityofchicago.org) hosts the [Building Footprints](https://data.cityofchicago.org/Buildings/Building-Footprints/syp8-uezg) dataset in CSV format; available at: <https://data.cityofchicago.org/api/views/syp8-uezg/rows.csv?accessType=DOWNLOAD>.

The "the_geom" column of the input CSV file contains WKT strings.

To assign UBIDs to the records in the input CSV file:

1. `uv run buildingid append2csv wkt --code-length=11 --fieldname-code="UBID" --fieldname-wktstr="the_geom" < rows.csv > rows.out.csv 2> rows.err.csv`

### San Jose, CA (historical example)

This example uses a historical `Basemap_2` archive.
The original city and download links returned HTTP 403 and have been removed.
File names and coordinate reference systems may differ in current downloads.

The City of San Jose previously provided datasets that included building footprints and land parcels.

The `Basemap_2` ZIP archive used in this example contains a building footprints dataset in Esri shapefile format.
Its coordinate system is NAD 1983 StatePlane California III FIPS 0403 Feet.

To convert the Esri shapefile into CSV format and then assign UBIDs to the resulting CSV file:

1. `ogr2ogr -s_srs "$(cat Basemap2_201905021152225992/BuildingFootprint.prj)" -t_srs "EPSG:4326" -f CSV BuildingFootprint.csv Basemap2_201905021152225992/BuildingFootprint.shp -lco GEOMETRY=AS_WKT`
2. `uv run buildingid append2csv wkt --code-length=11 --fieldname-code="UBID" --fieldname-wktstr="WKT" < BuildingFootprint.csv > BuildingFootprint.out.csv 2> BuildingFootprint.err.csv`

## License

[The 2-Clause BSD License](https://opensource.org/licenses/BSD-2-Clause)

## Contributions

Contributions are accepted on [GitHub](https://github.com/) via the fork and pull request workflow.
See [GitHub's pull request documentation](https://docs.github.com/en/pull-requests/reference/pull-requests) for more information.
