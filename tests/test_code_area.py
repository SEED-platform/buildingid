# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

from openlocationcode import openlocationcode

from buildingid.code import CodeArea


def test_buildingid_code_area_area():
    codeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -10.0,
        -10.0,
        10.0,
        10.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert codeArea.area == 400.0


def test_buildingid_code_area_intersection():
    codeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -10.0,
        -10.0,
        10.0,
        10.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )
    otherCodeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -5.0,
        -5.0,
        15.0,
        15.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    bbox = codeArea.intersection(otherCodeArea)

    assert bbox is not None
    assert bbox[0] == -5.0
    assert bbox[1] == -5.0
    assert bbox[2] == 10.0
    assert bbox[3] == 10.0


def test_buildingid_code_area_jaccard():
    codeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -10.0,
        -10.0,
        10.0,
        10.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )
    otherCodeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -5.0,
        -5.0,
        15.0,
        15.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert codeArea.jaccard(otherCodeArea) == 225.0 / (400.0 + 400.0 - 225.0)  # OK: intersects

    otherCodeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -20.0,
        -20.0,
        -10.0,
        -10.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert codeArea.jaccard(otherCodeArea) == 0.0  # OK: adjacent

    otherCodeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -30.0,
        -30.0,
        -20.0,
        -20.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    assert codeArea.jaccard(otherCodeArea) is None  # Fail: no intersection


def test_buildingid_code_area_resize():
    origCodeArea = CodeArea(
        openlocationcode.CodeArea(-1.0, -1.0, 1.0, 1.0, codeLength=openlocationcode.PAIR_CODE_LENGTH_),
        -10.0,
        -10.0,
        10.0,
        10.0,
        codeLength=openlocationcode.PAIR_CODE_LENGTH_,
    )

    newCodeArea = origCodeArea.resize()

    assert newCodeArea.centroid == origCodeArea.centroid
    assert newCodeArea.latitudeLo == -9.0
    assert newCodeArea.longitudeLo == -9.0
    assert newCodeArea.latitudeHi == 9.0
    assert newCodeArea.longitudeHi == 9.0
    assert newCodeArea.codeLength == origCodeArea.codeLength
