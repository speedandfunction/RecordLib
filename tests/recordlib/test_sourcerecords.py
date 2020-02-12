from RecordLib.sourcerecords import SourceRecord
import pytest
import os
from RecordLib.sourcerecords.summary.parse_pdf import parse_pdf

def test_create_from_parser():
    path = "tests/data/summaries"
    files = os.listdir(path)
    if not os.path.exists(path) or len(files) == 0:
        pytest.fail(f"Need to put example summary files at {path}")
    first = files[0]
    try:
        sr = SourceRecord(os.path.join(path, first), parser=parse_pdf)
        person = sr.person
        cases = sr.cases
    except Exception as e:
        pytest.fail(str(e))