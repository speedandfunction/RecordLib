from __future__ import annotations
from RecordLib.crecord import Person
from RecordLib.crecord import Case
from .parse_pdf import parse_pdf
from typing import Union, BinaryIO


class Docket:

    @staticmethod
    def from_pdf(pdf: Union[BinaryIO, str]) -> Docket:
        """ Create a Docket from a pdf file. """
        defendant, case, errors = parse_pdf(pdf)
        return Docket(defendant, case), errors

    def __init__(self, defendant: Person, case: Case) -> None:
        self._defendant = defendant
        self._case = case