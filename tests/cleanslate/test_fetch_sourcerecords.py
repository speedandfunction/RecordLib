"""
Tests for fetching sourcerecords, from SourceRecord objects that include urls. 
"""

import os
import pytest
from django.core.files import File
from cleanslate.models import SourceRecord
from cleanslate.serializers import SourceRecordSerializer, CRecordSerializer
from RecordLib.crecord import CRecord
from RecordLib.petitions import Expungement
from RecordLib.utilities.serializers import to_serializable


@pytest.mark.django_db
def test_download_ujs_docs(admin_client):
    """
    post a couple of documents with urls to the server. Server creates objects to store the downloaded files and then 
    returns uuids of the document objects in the database.
    """
    doc_1 = {
        "docket_num": "CP-12345",
        "court": "CP",
        "url": "https://ujsportal.pacourts.us/DocketSheets/CPReport.ashx?docketNumber=CP-25-CR-1234567-2010&dnh=12345",
        "caption": "Comm. v. SillyKitty",
        "record_type": SourceRecord.RecTypes.DOCKET_PDF,
    }
    doc_2 = {
        "docket_num": "CP-54321",
        "court": "CP",
        "url": "https://ujsportal.pacourts.us/DocketSheets/CourtSummaryReport.ashx?docketNumber=CP-25-CR-1234567-2010&dnh=12345",
        "caption": "Comm. v. SillyKitty",
        "record_type": SourceRecord.RecTypes.SUMMARY_PDF,
    }
    resp = admin_client.post(
        "/api/record/sourcerecords/fetch/",
        data={"source_records": [doc_1, doc_2]},
        follow=True,
        content_type="application/json",
    )
    assert resp.status_code == 200
    for rec in resp.data["source_records"]:
        try:
            rec["id"]
        except Exception:
            pytest.fail("rec in response didn't have an id")

