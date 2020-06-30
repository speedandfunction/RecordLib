"""
Testing api for sending a crecord and source records, parsing the source records, and integrating the info from the source records into 
the crecord
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
def test_integrate_sources_with_crecord(dclient, admin_user, example_crecord):
    """
    User can post source records and an empty crecord to the server and receive a 
    crecord with the cases from the source record incorporated.
    """
    dclient.force_authenticate(user=admin_user)
    docket = os.listdir("tests/data/dockets/")[0]
    with open(f"tests/data/dockets/{docket}", "rb") as d:
        doc_1 = SourceRecord.objects.create(
            caption="Hello v. World",
            docket_num="MC-1234",
            court=SourceRecord.Courts.CP,
            url="https://abc.def",
            record_type=SourceRecord.RecTypes.DOCKET_PDF,
            file=File(d),
            owner=admin_user,
        )
    summary = os.listdir("tests/data/summaries")[0]
    with open(f"tests/data/summaries/{summary}", "rb") as s:
        doc_2 = SourceRecord.objects.create(
            caption="Hello v. Goodbye",
            docket_num="MC-1235",
            court=SourceRecord.Courts.MDJ,
            url="https://def.ghi",
            record_type=SourceRecord.RecTypes.SUMMARY_PDF,
            file=File(s),
            owner=admin_user,
        )

    # when sent to api, serialized document data won't have a file included.
    # The request is asking to do stuff using the file that is on the server.
    doc_1_data = SourceRecordSerializer(doc_1).data
    # doc_1_data.pop("file")

    doc_2_data = SourceRecordSerializer(doc_2).data
    # doc_2_data.pop("file")
    source_records = [doc_1_data, doc_2_data]
    data = {
        "crecord": CRecordSerializer(example_crecord).data,
        "source_records": source_records,
    }

    resp = dclient.put("/api/record/cases/", data=data)
    assert resp.status_code == 200
    assert "crecord" in resp.data
    assert "source_records" in resp.data
    # the response source_records list might include new source records, so will be at
    # least as long as the original source records list.
    assert len(resp.data["source_records"]) >= len(source_records)
    try:

        CRecord.from_dict(resp.data["crecord"])
    except Exception as err:
        pytest.fail(err)

