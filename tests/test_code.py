# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import pytest
import shapely.wkt
from openlocationcode import openlocationcode

from buildingid.code import RE_PATTERN_, decode, encode, isValid


def test_buildingid_code_decode():
    with pytest.raises(ValueError, match="Invalid code"):
        decode(None)

    with pytest.raises(ValueError, match="Invalid code"):
        decode("")

    # # TODO
    # decode('6FG22222+22-0-0-0-0')

    # # TODO
    # decode('6FQ72222+22-40000-40000-40000-40000')


def test_buildingid_code_encode_when_geom_is_wkt_POINT():
    geom = shapely.wkt.loads("POINT (0 0)")

    (geom_bounds_min_x, geom_bounds_min_y, geom_bounds_max_x, geom_bounds_max_y) = geom.bounds

    geom_centroid = geom.centroid

    code = encode(
        geom_bounds_min_y,
        geom_bounds_min_x,
        geom_bounds_max_y,
        geom_bounds_max_x,
        geom_centroid.y,
        geom_centroid.x,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert code == "6FG22222+22-0-0-0-0"


def test_buildingid_code_encode_when_geom_is_wkt_POLYGON():
    geom = shapely.wkt.loads("POLYGON ((0 0, 0 10, 10 10, 10 0, 0 0))")

    (geom_bounds_min_x, geom_bounds_min_y, geom_bounds_max_x, geom_bounds_max_y) = geom.bounds

    geom_centroid = geom.centroid

    code = encode(
        geom_bounds_min_y,
        geom_bounds_min_x,
        geom_bounds_max_y,
        geom_bounds_max_x,
        geom_centroid.y,
        geom_centroid.x,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert code == "6FQ72222+22-40000-40000-40000-40000"


def test_buildingid_code_CodeArea_encode():
    geom = shapely.wkt.loads("POINT (0 0)")

    (geom_bounds_min_x, geom_bounds_min_y, geom_bounds_max_x, geom_bounds_max_y) = geom.bounds

    geom_centroid = geom.centroid

    origCode = encode(
        geom_bounds_min_y,
        geom_bounds_min_x,
        geom_bounds_max_y,
        geom_bounds_max_x,
        geom_centroid.y,
        geom_centroid.x,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    origCodeArea = decode(origCode)

    newCodeArea = origCodeArea.resize()

    newCode = newCodeArea.encode()

    assert origCode == newCode


def test_buildingid_code_isValid():
    assert not isValid(None)
    assert not isValid("")
    assert isValid("6FG22222+22-0-0-0-0")
    assert isValid("6FQ72222+22-40000-40000-40000-40000")


def test_buildingid_code_re():
    assert RE_PATTERN_.match("00000000+-0-0-0-0") is None
    assert RE_PATTERN_.match("00220000+-0-0-0-0") is None
    assert RE_PATTERN_.match("00002200+-0-0-0-0") is None
    assert RE_PATTERN_.match("00000022+-0-0-0-0") is None
    assert RE_PATTERN_.match("00000000+22-0-0-0-0") is None
    assert RE_PATTERN_.match("22000000+-0-0-0-0") is not None
    assert RE_PATTERN_.match("22000000+0-0-0-0-0") is None
    assert RE_PATTERN_.match("22000000+00-0-0-0-0") is not None
    assert RE_PATTERN_.match("22000000+000-0-0-0-0") is not None
    assert RE_PATTERN_.match("22220000+-0-0-0-0") is not None
    assert RE_PATTERN_.match("22220000+0-0-0-0-0") is None
    assert RE_PATTERN_.match("22220000+00-0-0-0-0") is not None
    assert RE_PATTERN_.match("22220000+000-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222200+-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222200+0-0-0-0-0") is None
    assert RE_PATTERN_.match("22222200+00-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222200+000-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+0-0-0-0-0") is None
    assert RE_PATTERN_.match("22222222+00-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+000-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+2-0-0-0-0") is None
    assert RE_PATTERN_.match("22222222+0-0-0-0-0") is None
    assert RE_PATTERN_.match("22222222+00-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+002-0-0-0-0") is None
    assert RE_PATTERN_.match("22222222+22-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+222-0-0-0-0") is not None
    assert RE_PATTERN_.match("22222222+2202-0-0-0-0") is None
    assert RE_PATTERN_.match("22222222+2220-0-0-0-0") is not None
