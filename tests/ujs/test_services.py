import pytest
from ujs.models import SourceRecord
from ujs.services import download
from ujs.services.UJSSearch import UJSSearch 
from datetime import datetime, date
import logging
import time
import requests


# TODO: mock this with the following,
#  if I can figure out a way for that still to be a worthwhile test. 
# [{'docket_number': 'CP-46-CR-0008423-2015', 'docket_sheet_url': 'CPReport.ashx?docketNumber=CP-46-CR-0008423-2015&dnh=ZvuxhBGDxBDVzE1TXOV00Q%3d%3d', 'summary_url': 'CourtSummaryReport.ashx?docketNumber=CP-46-CR-0008423-2015&dnh=ZvuxhBGDxBDVzE1TXOV00Q%3d%3d', 'caption': 'Comm. v. Kane, Kathleen Granahan', 'case_status': 'Closed', 'otn': 'T7090322', 'dob': '6/14/1966'}, {'docket_number': 'CP-46-MD-0002457-2015', 'docket_sheet_url': 'CPReport.ashx?docketNumber=CP-46-MD-0002457-2015&dnh=IKyQqgkSTZdotOIfTavQwQ%3d%3d', 'summary_url': 'CourtSummaryReport.ashx?docketNumber=CP-46-MD-0002457-2015&dnh=IKyQqgkSTZdotOIfTavQwQ%3d%3d', 'caption': 'Comm v  Kane, Kathleen Granahan', 'case_status': 'Closed', 'otn': 'T7090322', 'dob': '6/14/1966'}, {'docket_number': 'CP-46-CR-0006239-2015', 'docket_sheet_url': 'CPReport.ashx?docketNumber=CP-46-CR-0006239-2015&dnh=ljFLOabFyPEOG9nfpg%2bOTA%3d%3d', 'summary_url': 'CourtSummaryReport.ashx?docketNumber=CP-46-CR-0006239-2015&dnh=ljFLOabFyPEOG9nfpg%2bOTA%3d%3d', 'caption': 'Comm. v. Kane, Kathleen Granahan', 'case_status': 'Closed', 'otn': 'T6863802', 'dob': '6/14/1966'}]


def test_cp_search():
    cp_searcher = UJSSearch.use_court("CP")
    results = cp_searcher.search_name(
        last_name="Kane", first_name="Kathleen", 
        dob=date(year=1966, month=6, day=14))
    assert len(results) > 0 
    try:
        for r in results:
            r["docket_number"]
    except KeyError:
        pytest.raises("Search Results missing docket number.")

def test_cp_search_no_results():
    cp_searcher = UJSSearch.use_court("CP")
    results = cp_searcher.search_name(
        first_name="Ferocity", last_name="Wimbledybear") 
    assert len(results) == 0 
 


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
