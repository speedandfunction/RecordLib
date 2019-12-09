import pytest
from grades.models import ChargeRecord

@pytest.fixture
def example_charge_record():
    cr = ChargeRecord(
        offense = "Wearing too many socks",
        title = "18",
        section = "1234",
        subsection = "b4",
        grade = "M1",
    )
    return cr

