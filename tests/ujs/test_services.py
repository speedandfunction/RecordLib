import pytest
from ujs.models import SourceRecord
from ujs.services import download
from ujs.services.UJSSearch import UJSSearch,CPSearch
from datetime import datetime, date
import logging
import time
import requests
import os

def test_cp_search(monkeypatch):

    def get_results(*args, **kwargs):
        return [
            {
                'docket_number': 'CP-11-CR-0001111-2015', 
                'docket_sheet_url': 'CPReport.ashx?docketNumber=xxx', 
                'summary_url': 'CourtSummaryReport.ashx?docketNumber=yyy',
                'caption': 'Comm. v. Normal', 
                'case_status': 'Closed',
                'otn': 'Txxxx', 
                'dob': '1/11/1940'
            }, 
        ]

    if os.environ.get("REAL_NETWORK_TESTS") != "TRUE":
        monkeypatch.setattr(CPSearch,"search_name", get_results)
    
    first_name = os.environ.get("UJS_SEARCH_TEST_FNAME") or "Joe"
    last_name = os.environ.get("UJS_SEARCH_TEST_LNAME") or "Normal"
    dob = datetime.strptime(os.environ.get("UJS_SEARCH_TEST_DBO"), r"%Y-%m-%d") ) or date(2001, 1, 1))

    cp_searcher = UJSSearch.use_court("CP")
    results = cp_searcher.search_name(
        last_name=last_name, first_name=first_name, 
        dob=dob)
    assert len(results) > 0 
    try:
        for r in results:
            r["docket_number"]
    except KeyError:
        pytest.raises("Search Results missing docket number.")


def test_cp_search_no_results(monkeypatch):

    def get_results(*args, **kwargs):
        return []

    if os.environ.get("REAL_NETWORK_TESTS") != "TRUE":
        monkeypatch.setattr(CPSearch, "search_name", get_results)
    cp_searcher = UJSSearch.use_court("CP")
    results = cp_searcher.search_name(
        first_name="Ferocity", last_name="Wimbledybear") 
    assert len(results) == 0 


def test_mdj_search():
    md_searcher = UJSSearch.use_court("MDJ")
    results = cp_searcher.search_name(
        last_name="Kane", first_name="Kathleen", 
        dob=date(year=1966, month=6, day=14))
    assert len(results) == 2
    try:
        for r in results:
            r["docket_number"]
    except KeyError:
        pytest.raises("Search Results missing docket number.")



class FakeResponse:

    def __init__(self):
        self.content = b'some bytes content'
        self.status_code = 200


def test_download_source_records(admin_user, monkeypatch):

    def slow_get(*args, **kwargs):
        time.sleep(3)
        return FakeResponse()

    monkeypatch.setattr(requests, 'get', slow_get)

    rec = SourceRecord.objects.create(
        caption="Test v Test",
        docket_num="CP-1234",
        court=SourceRecord.Courts.CP,
        url="https://some.slow.url",
        record_type=SourceRecord.RecTypes.SUMMARY_PDF,
        owner=admin_user,
    )
    rec.save()
    assert rec.file.name is None
    before = datetime.now()
    recs = [
        rec, rec, rec
    ]
    download.source_records(recs)
    after = datetime.now()
    time_spent = after - before
    assert rec.file.name is not None
    # use pytest --log-cli-level info to see this.
    logging.info(f"downloading {len(recs)} document took {time_spent.total_seconds()} seconds.")
