from django.test import TestCase
from django.core.files import File
from cleanslate.models import ExpungementPetitionTemplate, SealingPetitionTemplate, SourceRecord
from RecordLib.petitions import Expungement
import pytest
import io
from django.db import IntegrityError
from django.contrib.auth.models import User

# django unittest test, for testing the database and relying on django's built in db setup/teardowns.
class PetitionTemplateTestCase(TestCase):
    def setUp(self):
        with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
            ExpungementPetitionTemplate.objects.create(name="Expungement Petition Template", file=File(tp))

    def test_petition_template_type(self):
        """  A petition template has a doctype"""
        expungement_template = ExpungementPetitionTemplate.objects.get(name="Expungement Petition Template")
        self.assertEqual(expungement_template.name, "Expungement Petition Template")


# a pytest test, so i can use the fixtures
@pytest.mark.django_db
def test_render_petition(example_expungement):
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        pet = ExpungementPetitionTemplate.objects.create(
            name="Expungement Petition Template", file=File(tp))
        example_expungement.set_template(pet.file)
    try:
        example_expungement.render()
    except Exception as e:
        pytest.fail(str(e))
        


@pytest.mark.django_db
def test_single_default_petition():
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        pet1 = ExpungementPetitionTemplate.objects.create(
            name="Expungement Petition Template", file=File(tp))
    with open("tests/templates/791SealingTemplate.docx", "rb") as tp:
        pet2 = ExpungementPetitionTemplate.objects.create(
            name="Another expungement template", file=File(tp)
        )
    pet1.default = True
    pet1.save()
    with pytest.raises(IntegrityError):
        pet2.default = True
        pet2.save()

@pytest.mark.django_db    
def test_new_user_has_default_petitions():
    with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
        ExpungementPetitionTemplate.objects.create(
            name="Expungement Petition Template", file=File(tp), default=True)
    with open("tests/templates/791SealingTemplate.docx", "rb") as tp:
        SealingPetitionTemplate.objects.create(
            name="Sealing Template", file=File(tp), default=True
        )
    new_user = User.objects.create_user("testuser", password="test")
    new_user.save()
    assert new_user.userprofile.expungement_petition_template.name == "Expungement Petition Template"
    assert new_user.userprofile.sealing_petition_template.name == "Sealing Template"
    

pytest.mark.django_db
def test_create_source_record(admin_user):
    rec_model = SourceRecord(
        caption="Comm. v. Smith",
        docket_num="CP-1234", 
        court=SourceRecord.Courts.CP,
        url="https://ujsportal.gov", 
        record_type=SourceRecord.RecTypes.SUMMARY_PDF,
        owner=admin_user)
    rec_model.save()
    new_id = rec_model.id
    saved_model = SourceRecord.objects.get(id=new_id)
    assert saved_model.caption == "Comm. v. Smith"
    assert saved_model.fetch_status == SourceRecord.FetchStatuses.NOT_FETCHED
    assert saved_model.parse_status == SourceRecord.ParseStatuses.UNKNOWN