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
        """Factory method to create a Summary from a pdf."""
        defendant, cases, errors = parse_pdf(pdf)
        return Summary(defendant, cases), errors

    def __init__(self, defendant: Person = None, cases: List = None) -> None:
        self._defendant = defendant
        self._cases = cases

    def get_defendant(self) -> Person:
        """ Get the Defendant a Summary relates to."""
        return self._defendant

    def get_cases(self) -> List:
        """Get the set of cases that a Summary describes"""
        return self._cases
