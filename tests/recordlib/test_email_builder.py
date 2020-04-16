from RecordLib.utilities.email_builder import EmailBuilder
from RecordLib.analysis import Analysis
from datetime import date
from RecordLib.analysis.ruledefs.petition_rules import seal_convictions

def test_unsealable_until_date(example_crecord):
    example_crecord.cases[0].disposition_date = date(2020, 1,1)
    analysis = Analysis(example_crecord).rule(seal_convictions)
    eb = EmailBuilder([], analysis)
    assert eb.get_unsealable_until_date(example_crecord.cases[0]) is not None