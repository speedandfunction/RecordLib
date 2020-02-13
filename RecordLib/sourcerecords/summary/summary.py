from __future__ import annotations
from typing import List, Union, BinaryIO
from RecordLib.crecord.person import Person
from .parse_pdf import parse_pdf

class Summary:
    """
    Track information about a summary.
    """

    @staticmethod
    def from_pdf(pdf: Union[BinaryIO, str]):
        defendant, cases, errors, parsed_tree = parse_pdf(pdf)
        return Summary(defendant, cases)

    def __init__(self, defendant: Person = None, cases: List = None) -> None:
        self._defendant = defendant
        self._cases = cases

    def get_defendant(self) -> Person:
        return self._defendant

    def get_cases(self) -> List:
        return self._cases
