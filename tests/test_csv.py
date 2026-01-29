# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import io
import re

import pytest
from openlocationcode import openlocationcode

from buildingid.command_line.dict_decoders import LatLngDictDecoder, WKBDictDecoder, WKTDictDecoder
from buildingid.command_line.dict_encoders import BaseGeometryDictEncoder, ErrorDictEncoder
from buildingid.command_line.dict_pipe import DictPipe
from buildingid.command_line.exceptions import FieldNotFoundError, FieldNotUniqueError


def test_buildingid_csv_DictPipe_LatLngDictDecoder_FieldNotFoundError():
    decoder_in = LatLngDictDecoder("Latitude", "Longitude")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("x,Longitude")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotFoundError, match=re.escape("field 'Latitude' is not defined")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("Latitude,x")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotFoundError, match=re.escape("field 'Longitude' is not defined")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_WKBDictDecoder_FieldNotFoundError():
    decoder_in = WKBDictDecoder("WKB")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("x")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotFoundError, match=re.escape("field 'WKB' is not defined")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_WKTDictDecoder_FieldNotFoundError():
    decoder_in = WKTDictDecoder("WKT")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("x")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotFoundError, match=re.escape("field 'WKT' is not defined")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_LatLngDictDecoder_FieldNotUniqueError():
    decoder_in = LatLngDictDecoder("Latitude", "Longitude")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("Latitude,Longitude,UBID")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("Latitude,Longitude,UBID_Error_Name")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Name' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("Latitude,Longitude,UBID_Error_Message")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Message' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_WKBDictDecoder_FieldNotUniqueError():
    decoder_in = WKBDictDecoder("WKB")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("WKB,UBID")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("WKB,UBID_Error_Name")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Name' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("WKB,UBID_Error_Message")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Message' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_WKTDictDecoder_FieldNotUniqueError():
    decoder_in = WKTDictDecoder("WKT")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("WKT,UBID")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("WKT,UBID_Error_Name")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Name' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    io_in = io.StringIO("WKT,UBID_Error_Message")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    with pytest.raises(FieldNotUniqueError, match=re.escape("field 'UBID_Error_Message' has already been taken")):
        dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})


def test_buildingid_csv_DictPipe_LatLngDictDecoder():
    decoder_in = LatLngDictDecoder("Latitude", "Longitude")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("Latitude,Longitude\r\n0,0\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "Latitude,Longitude\r\n0,0\r\n"
    assert io_out.getvalue() == "Latitude,Longitude,UBID\r\n0,0,6FG22222+22-0-0-0-0\r\n"
    assert io_err.getvalue() == ""

    io_in = io.StringIO("Latitude,Longitude\r\nx,x\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "Latitude,Longitude\r\nx,x\r\n"
    assert io_out.getvalue() == ""
    assert (
        io_err.getvalue()
        == "Latitude,Longitude,UBID_Error_Name,UBID_Error_Message\r\nx,x,ValueError,could not convert string to float: 'x'\r\n"
    )


def test_buildingid_csv_DictPipe_WKBDictDecoder():
    decoder_in = WKBDictDecoder("WKB")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("WKB\r\n010100000000000000000000000000000000000000\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "WKB\r\n010100000000000000000000000000000000000000\r\n"
    assert io_out.getvalue() == "WKB,UBID\r\n010100000000000000000000000000000000000000,6FG22222+22-0-0-0-0\r\n"
    assert io_err.getvalue() == ""

    io_in = io.StringIO("WKB\r\nx\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "WKB\r\nx\r\n"
    assert io_out.getvalue() == ""
    assert io_err.getvalue() == "WKB,UBID_Error_Name,UBID_Error_Message\r\nx,GEOSException,ParseException: Unexpected EOF parsing WKB\r\n"


def test_buildingid_csv_DictPipe_WKTDictDecoder():
    decoder_in = WKTDictDecoder("WKT")

    encoder_out = BaseGeometryDictEncoder("UBID", openlocationcode.PAIR_CODE_LENGTH_)

    encoder_err = ErrorDictEncoder("UBID")

    dict_pipe = DictPipe(decoder_in, encoder_out, encoder_err)

    io_in = io.StringIO("WKT\r\nPOINT (0 0)\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "WKT\r\nPOINT (0 0)\r\n"
    assert io_out.getvalue() == "WKT,UBID\r\nPOINT (0 0),6FG22222+22-0-0-0-0\r\n"
    assert io_err.getvalue() == ""

    io_in = io.StringIO("WKT\r\nx\r\n")
    io_out = io.StringIO("")
    io_err = io.StringIO("")

    dict_pipe.run(io_in, io_out, io_err, args_in=[], kwargs_in={}, args_out=[], kwargs_out={})

    assert io_in.getvalue() == "WKT\r\nx\r\n"
    assert io_out.getvalue() == ""
    assert io_err.getvalue() == "WKT,UBID_Error_Name,UBID_Error_Message\r\nx,GEOSException,ParseException: Unknown type: 'X'\r\n"
