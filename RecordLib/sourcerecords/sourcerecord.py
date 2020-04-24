from typing import Any, Callable, Optional

def null_parser(src):
    """
    A blank parser that returns the right shape of nothing for a sourcerecord.
    """
    return None, None, ["No parser used"], None

class SourceRecord:
    """
    A generic class for tranforming raw inputs with information about cases and criminal records into
    structured objects.
    """



    def __init__(self, src: Any, parser: Optional[Callable] = None): 
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
        Returns:
            A 4-tuple:
                person: the Person that the source relates to.
                cases: the set of Cases that the source relates to.
                errors: parsing errors.
                parsed_source: if the parser creates a syntax tree out of the source, for example.
        """
        self.raw_source = src
        self.parser = parser or null_parser
        try: 
            person, cases, errors = self.parser(src)
            parsed_source=None
        except ValueError as e:
            # The PEG parsers also return the xml tree of parsed data, which can be useful to have.
            person, cases, errors, raw_source = self.parser(src)
        self.parsed_source = parsed_source
        self.person = person
        self.cases = cases
        self.errors = errors
