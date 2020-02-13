from datetime import datetime
from cleanslate.models import SourceRecord
from typing import List
import requests
from django.core.files.base import ContentFile

import urllib3
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'




def source_records(records: List[SourceRecord]) -> None:
    """ Download the source records in a list of source records, if they're not already present. 
    
    TODO: fetch these urls asynchronously.
    """
    for rec in records:
        if rec.file._file is None:
            resp = requests.get(rec.url, headers={"User-Agent": "ExpungmentGeneratorTesting"})
            if resp.status_code == 200:
                rec.file.save(f"{rec.id}.pdf", ContentFile(resp.content))
                rec.fetch_status = SourceRecord.FetchStatuses.FETCHED
                rec.save()
            else:
                rec.fetch_status = SourceRecord.FetchStatuses.FETCH_FAILED
                rec.save()