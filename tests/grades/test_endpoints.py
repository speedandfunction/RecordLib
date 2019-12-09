import pytest
import copy
from grades.models import ChargeRecord


@pytest.mark.django_db
def test_create_chargerecords(admin_client):
    resp = admin_client.post("/grades/", {
        "offense": "Ice skating without proper snacks",
        "title": "15",
        "section": "iii",
        "grade": "M1"
    })
    assert resp.status_code == 201
    recs = ChargeRecord.objects.all()
    assert len(recs) == 1
    assert recs[0].grade == 'M1'



def test_guess_grade(admin_client, example_charge_record):
    cr1 = copy.copy(example_charge_record)
    cr1.grade = "M"
    cr1.save()

    cr2 = copy.copy(example_charge_record)
    cr2.grade = "M1"
    cr2.save()

    resp = admin_client.get(f"/grades/guess/", data = {
        "offense": example_charge_record.offense,
        "title": example_charge_record.title,
        "section": example_charge_record.section,
        "subsection": example_charge_record.subsection,
    })

    assert resp.status_code == 200
    predictions = resp.data
    assert list(filter(lambda i: i[0] == "M", predictions))[0][1] == 0.5
    assert list(filter(lambda i: i[0] == "M1", predictions))[0][1] == 0.5    


def test_guess_grade_no_subsection(admin_client, example_charge_record):
    cr1 = copy.copy(example_charge_record)
    cr1.subsection = "iii"
    cr1.grade = "M"
    cr1.save()

    cr2 = copy.copy(example_charge_record)
    cr2.grade = "M1"
    cr2.subsection = ""
    cr2.save()

    resp = admin_client.get(f"/grades/guess/", data = {
        "offense": example_charge_record.offense,
        "title": example_charge_record.title,
        "section": example_charge_record.section
    })

    assert resp.status_code == 200
    predictions = resp.data
    assert list(filter(lambda i: i[0] == "M1", predictions))[0][1] == 1
    assert predictions == [('M1', 1)]
    assert predictions[0][0] ==  "M1"

