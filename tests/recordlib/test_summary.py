"""
Testing the RecordLib Summary class.
"""

import os
from datetime import date, timedelta
import logging
import pytest
from RecordLib.sourcerecords import Summary
from RecordLib.crecord import CRecord, Person, Case


def test_init():
    try:
        Summary.from_pdf(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
    except Exception:
        pytest.fail("Creating Summary object failed.")


def test_parse_pdf_from_file():
    summary, _ = Summary.from_pdf(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
    assert len(summary.get_cases()) > 0


def test_parse_pdf_from_path():
    summary, _ = Summary.from_pdf(pdf="tests/data/CourtSummaryReport.pdf")
    assert len(summary.get_cases()) > 0


def test_bulk_parse_pdf_from_path(caplog):
    caplog.set_level(logging.INFO)
    paths = os.listdir("tests/data/summaries")
    if len(paths) == 0:
        pytest.fail("No summaries to parse in /tests/data/summaries.")
    fails = []
    logging.info("Successful parses:")
    for path in paths:
        try:
            summary, _ = Summary.from_pdf(
                pdf=os.path.join(f"tests/data/summaries", path)
            )
            logging.info(path)
        except Exception:
            print(path)
            fails.append(os.path.split(path)[1])
    if len(fails) > 0:
        logging.error(f"{ len(fails) } / {len(paths)} summaries failed to parse:")
        for fail in fails:
            logging.error(f"  - {fail}")
        pytest.fail("Summaries failed to parse.")


def test_add_summary_to_crecord():
    summary, _ = Summary.from_pdf(pdf="tests/data/CourtSummaryReport.pdf")
    rec = CRecord(Person("John", "Smith", date(1998, 1, 1)))
    rec.add_summary(summary, override_person=True)
    assert len(rec.person.first_name) > 0
    assert rec.person.first_name != "John"


def test_get_defendant():
    summary, _ = Summary.from_pdf(pdf="tests/data/CourtSummaryReport.pdf")
    assert len(summary.get_defendant().first_name) > 0
    assert len(summary.get_defendant().last_name) > 0
    assert summary.get_defendant().date_of_birth > date(1900, 1, 1)


def test_get_cases():
    summary, _ = Summary.from_pdf(pdf="tests/data/CourtSummaryReport.pdf")
    assert len(summary.get_cases()) > 0
    assert len(summary.get_cases()) > 0
    assert isinstance(summary.get_cases()[0], Case)


def test_get_sentences():
    summary, _ = Summary.from_pdf(pdf="tests/data/CourtSummaryReport.pdf")
    cases = summary.get_cases()
    for case in cases:
        for charge in case.charges:
            for sentence in charge.sentences:
                try:
                    assert (
                        isinstance(sentence.sentence_length.max_time, timedelta)
                        or sentence.sentence_length.max_time is None
                    )
                except Exception:
                    pytest.fail("Could not get sentence from charge.")


def test_get_arrest_date():
    """ We can get the arrest date from a summary's cases"""
    summary, _ = Summary.from_pdf(pdf=open("tests/data/CourtSummaryReport.pdf", "rb"))
    cases = summary.get_cases()
    # There's not a standard example summary pdf to run tests on, so can't assume much about the contents of
    # the summary being parsed here.
    # In the summary being parsed, an arrest date might be missing from a case,
    # but its unlikely there's _no_ case with an arrest date.
    # If you're testing this on a summary that has no arrest dates ...
    # find a different summary to use for testing.
    arrest_dates = [case.arrest_date for case in cases if case.arrest_date is not None]
    assert len(arrest_dates) > 0
