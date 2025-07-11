#
# pnnl-buildingid: buildingid/command_line/dict_encoders.py
#
# Copyright (c) 2019, Battelle Memorial Institute
# All rights reserved.
#
# See LICENSE.txt and WARRANTY.txt for details.

import typing

from .dict_datum import DictDatum
from .dict_pipe import DictEncoder


class BaseGeometryDictEncoder(DictEncoder[DictDatum]):
    def __init__(self, fieldname_code: str, code_length: int) -> None:
        super(BaseGeometryDictEncoder, self).__init__()

        self.fieldname_code = fieldname_code

        self.code_length = code_length

    def encode(self, datum: DictDatum) -> typing.Dict[str, typing.Any]:
        code = datum.encode(codeLength=self.code_length)

        row = {}

        row[self.fieldname_code] = code

        return row

    @property
    def fieldnames(self) -> typing.List[str]:
        return [
            self.fieldname_code,
        ]


class ErrorDictEncoder(DictEncoder[BaseException]):
    def __init__(self, fieldname_code: str) -> None:
        super(ErrorDictEncoder, self).__init__()

        self.fieldname_code = fieldname_code

    def encode(self, exception: BaseException) -> typing.Dict[str, typing.Any]:
        row = {}

        row[f"{self.fieldname_code}_Error_Name"] = type(exception).__name__
        row[f"{self.fieldname_code}_Error_Message"] = str(exception)

        return row

    @property
    def fieldnames(self) -> typing.List[str]:
        return [
            f"{self.fieldname_code}_Error_Name",
            f"{self.fieldname_code}_Error_Message",
        ]
