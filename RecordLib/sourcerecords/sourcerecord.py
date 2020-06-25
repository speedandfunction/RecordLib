from typing import Any, Callable, Optional
import re


def null_parser(_):
    """
    A blank parser that returns the right shape of nothing for a sourcerecord.
    """
    return None, None, ["No parser used"]


class SourceRecord:
    """
    A generic class for tranforming raw inputs with information about cases and criminal records into
    structured objects.
    """

    class RECORD_TYPES:
        SUMMARY = "SUMMARY"
        DOCKET = "DOCKET"

    def __init__(
        self,
        src: Any,
        parser: Optional[Callable] = None,
        record_type: Optional[str] = None,
    ):
        """
        Create a new SourceRecord with some data and a callable parser that can parse the source data.

        For example, if the `src` is a path to a summary pdf, then `parser` should be a function that
        accepts a path to a summary pdf and returns a tuple with certain values.

        Example:
            def bad_parser(txt): 
                return Person("Joe"), [Case(statute="18 1234")], [], txt

            sourcerecord = SourceRecord(sometext, parser=bad_parser)
            len(sourcerecord.cases) == 1
            sourcerecord.person.name == "Joe"

        Args: 
            src: data that contains information related to a criminal record.
            parser: a callable that can extract useful structured information from src.
            record_type: Identifies this source as a docket or a summary.
        Returns:
            A 4-tuple:
                person: the Person that the source relates to.
                cases: the set of Cases that the source relates to.
                errors: parsing errors.
                parsed_source: if the parser creates a syntax tree out of the source, for example.
        """
        self.raw_source = src
        self.parser = parser or null_parser
        person, cases, errors = self.parser(src)
        self.person = person
        self.cases = cases or []
        self.errors = errors
        self.record_type = record_type
