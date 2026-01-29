# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

from openlocationcode import openlocationcode

from buildingid.validators import (
    isValidCodeArea,
    isValidCodeLength,
    isValidLatitude,
    isValidLatitudeCenter,
    isValidLongitude,
    isValidLongitudeCenter,
)


def test_buildingid_validators_isValidCodeArea():
    assert isValidCodeArea(openlocationcode.CodeArea(0, 0, 1, 1, codeLength=openlocationcode.PAIR_CODE_LENGTH_))


def test_buildingid_validators_isValidCodeLength():
    assert not isValidCodeLength(0)
    assert not isValidCodeLength(1)
    assert isValidCodeLength(2)
    assert not isValidCodeLength(3)
    assert isValidCodeLength(4)
    assert not isValidCodeLength(5)
    assert isValidCodeLength(6)
    assert not isValidCodeLength(7)
    assert isValidCodeLength(8)
    assert not isValidCodeLength(9)
    assert isValidCodeLength(10)
    assert isValidCodeLength(11)


def test_buildingid_validators_isValidLatitude():
    assert isValidLatitude(0, 1)
    assert not isValidLatitude(1, 0)


def test_buildingid_validators_isValidLatitudeCenter():
    assert isValidLatitudeCenter(0, 2, 1)
    assert not isValidLatitudeCenter(0, 1, 2)


def test_buildingid_validators_isValidLongitude():
    assert isValidLongitude(0, 1)
    assert not isValidLongitude(1, 0)


def test_buildingid_validators_isValidLongitudeCenter():
    assert isValidLongitudeCenter(0, 2, 1)
    assert not isValidLongitudeCenter(0, 1, 2)
