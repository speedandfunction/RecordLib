from datetime import datetime
from cleanslate.models import SourceRecord
from typing import List
import requests
from django.core.files.base import ContentFile
from ujs_search.services import searchujs
import logging
import urllib3

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += "HIGH:!DH:!aNULL"
logger = logging.getLogger(__name__)


def source_records(records: List[SourceRecord]) -> None:
    """ Download the source records in a list of source records, if they're not already present. 
    
    TODO: fetch these urls asynchronously.
    """
    for rec in records:
        if rec.file._file is None:
            resp = requests.get(
                rec.url, headers={"User-Agent": "ExpungmentGeneratorTesting"}
            )
            if resp.status_code == 200:
                rec.file.save(f"{rec.id}.pdf", ContentFile(resp.content))
                rec.fetch_status = SourceRecord.FetchStatuses.FETCHED
                rec.save()
            else:
                rec.fetch_status = SourceRecord.FetchStatuses.FETCH_FAILED
                rec.save()


def dockets(docket_nums: List[str], owner: "User") -> [SourceRecord]:
    """
    Download the dockets in `docket_nums` and create SourceRecords for them.
    
    Return the list of newly generated source records.
    TODO do this asynchronously.
    """
    new_source_records = []
    for docket_number in docket_nums:
        try:
            result = searchujs.search_by_docket(docket_number)[0]
            new_source_record = SourceRecord(
                caption=result["caption"],
                docket_num=result["docket_number"],
                url=result["docket_sheet_url"],
                record_type=SourceRecord.RecTypes.DOCKET_PDF,
                owner=owner,
            )
            new_source_records.append(new_source_record)
        except Exception as err:
            logger.error("Downloading docket %s failed: %s", docket_number, str(err))
    # download all these new source records.
    source_records(new_source_records)
    return new_source_records

