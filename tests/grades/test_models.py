import pytest
import copy
from grades.models import ChargeRecord


def test_create_charge_record(example_charge_record):
    assert example_charge_record.weight == 1
    assert example_charge_record.section == "1234"




