
from RecordLib.sourcerecords.parsingutilities import get_text_from_pdf
from typing import Union, BinaryIO, Tuple, Callable, List, Optional

def parse_mdj_pdf(path: str) -> Tuple[Person, [Case], List[str], etree.Element]:
    """
    Parse an mdj docket, given the path to the docket pdf.

    This function uses the original Expungement Generator's technique: regexes and nested loops.
    """
    pass
