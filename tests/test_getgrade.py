import pytest
from RecordLib.guess_grade import guess_grade
from RecordLib.common import Charge

@pytest.mark.parametrize(
    "statute,grade",
    [("10 § 162.12", "M1"),
     ("10 § 162.15 §§ A1", "M1"),
     ("18 § 3922 §§ A1", "F3"),
     ("18 § 4904 §§ A1", "M2")]
)
def test_guess_grade(statute, grade):
    dummy_charge = Charge(offense="", grade="", statute=statute, sentences=[], disposition="")
    g, p = guess_grade(dummy_charge)
    assert g == grade
