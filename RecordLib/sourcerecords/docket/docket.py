from __future__ import annotations
from RecordLib.crecord import Person
from RecordLib.crecord import Case
from typing import Union, BinaryIO, List, Tuple
from RecordLib.sourcerecords.docket.re_parse_pdf import re_parse_pdf


class Docket:
    @staticmethod
    def from_pdf(pdf: Union[BinaryIO, str]) -> Tuple[Docket, List[str]]:
        """ Create a Docket from a pdf file. """
        defendant, cases, errors = re_parse_pdf(pdf)
        # parse functions always return a 4-tuple, (defendant, a list of cases, a list of errors, and optionally some raw parsed source.)
        # a docket, by definition, is only about one case, so we take the 0th element of the case list that this parser returns.
        return Docket(defendant, cases[0]), errors

    def __init__(self, defendant: Person, case: Case) -> None:
        self._defendant = defendant
        self._case = case
