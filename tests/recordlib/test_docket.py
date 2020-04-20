from RecordLib.sourcerecords import Docket, SourceRecord
from RecordLib.crecord import Person
from RecordLib.crecord import Case
import pytest
import os
import logging
from RecordLib.sourcerecords.docket.parse_mdj_pdf import parse_mdj_pdf

def test_pdf_factory_one():
    try:
        filename = os.listdir("tests/data/dockets")[0]
        dk, _ = Docket.from_pdf(os.path.join("tests/data/dockets", filename))
    except Exception as e:
        pytest.fail("Cannot create Docket object")
    assert isinstance(dk._case, Case)
    assert isinstance(dk._defendant, Person)
    assert dk._case.affiant is not None
    assert dk._defendant.aliases is not None
    assert dk._case.arresting_agency is not None



def test_pdf_factory_bulk(caplog):
    """
    Test parsing a whole directory of dockets.

    N.B. This doesn't currently report a failure if a _section_ of a docket failed to parse. 

    Run w/ `pytest tests/test_docket.py -k bulk -v -o log_cli=true` to show logging, even when test
    doesn't fail. Useful because sections can fail w/out causing the test to fail.
    """
    caplog.set_level(logging.INFO)
    files = os.listdir("tests/data/dockets")
    total_dockets = len(files)
    successes = 0
    error_list = []
    breakpoint()
    for f in files:
        try:
            logging.info(f"Parsing {f}")
            _, errs = Docket.from_pdf(os.path.join("tests/data/dockets", f))
            if len(errs) > 0:
                error_list = error_list + [(f, errs)]
            successes += 1
            logging.info(f"    {f} parsed.")
        except Exception as e:
            logging.error(f"    {f} failed to parse.")
    
    if len(error_list) > 0:
        logging.error(f"{len(error_list)} of {len(files)} cases had non-fatal parsing errors.")
        pytest.fail(f"{len(error_list)} of {len(files)} cases had non-fatal parsing errors.")
    if successes < total_dockets:
        logging.error(f"Only {successes}/{total_dockets} parsed.")
        pytest.fail(f"Only {successes}/{total_dockets} parsed.")



def test_mdj_docket_pdf_parser():
    path = os.path.join("tests","data","dockets")
    files = os.listdir(path)
    mdj_dockets = list(filter(lambda f: "MJ" in f, files))
    if len(mdj_dockets) == 0:
        pytest.fail("You need an MDJ docket named like MJ-........pdf for this test to pass.")
    for f in mdj_dockets:
        try:
            sr = SourceRecord(os.path.join(path, f), parser=parse_mdj_pdf)
        except Exception as e:
            pytest.fail(str(e))
        assert len(sr.cases) == 1 