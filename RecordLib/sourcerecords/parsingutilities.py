from typing import Union, BinaryIO, Optional
import os
import tempfile
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

def get_text_from_pdf(pdf: Union[BinaryIO, str]) -> str:
    """
    Function which extracts the text from a pdf document.
    Args:
        pdf:  Either a file object or the location of a pdf document.
        tempdir:  Place to store intermediate files.


    Returns:
        The extracted text of the pdf.
    """
    with tempfile.TemporaryDirectory() as out_dir:
        if hasattr(pdf, "read"):
            # the pdf attribute is a file object,
            # and we need to write it out, for pdftotext to use it.
            pdf_path = os.path.join(out_dir, "tmp.pdf")
            with open(pdf_path, "wb") as f:
                f.write(pdf.read())
        else:
            pdf_path = pdf
        # TODO - remove the option of making tempdir anything other than a tempfile. 
        #        Only doing it this way to avoid breaking old tests that send tempdir.
        #out_path = os.path.join(tempdir, "tmp.txt")
        out_path = os.path.join(out_dir, "tmp.txt")
        os.system(f'pdftotext -layout -enc "UTF-8" { pdf_path } { out_path }')
        try:
            with open(os.path.join(out_dir, "tmp.txt"), "r", encoding="utf8") as f:
                text = f.read()
                return text
        except IOError as e:
            logger.error("Cannot extract pdf text..")
            return ""

def date_or_none(date_text: str, fmtstr: str = r"%m/%d/%Y") -> datetime:
    """
    Return date or None given a string.
    """
    try:
        return datetime.strptime(date_text.strip(), fmtstr).date()
    except (ValueError, AttributeError):
        return None


def money_or_none(money_str: str) -> Optional[float]:
    try:
        return float(
            money_str.strip().replace(",","")
        )
    except:
        return None
