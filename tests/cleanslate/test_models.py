from django.test import TestCase
from cleanslate.models import PetitionTemplate


class PetitionTemplateTestCase(TestCase):
    def setUp(self):
        with open("tests/templates/790ExpungementTemplate_usingpythonvars.docx", 'rb') as tp:
            PetitionTemplate.objects.create(name="Expungement Petition Template", data=tp.read(), doctype="docx")

    def test_petition_template(self):
        """  A petition template has a doctype"""
        expungement_template = PetitionTemplate.objects.get(name="Expungement Petition Template")
        self.assertEqual(expungement_template.doctype, "docx")

