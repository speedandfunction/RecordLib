from django.test import TestCase
from cleanslate.models import PetitionTemplate


class PetitionTemplateTestCase(TestCase):
    def setUp(self):
        with open("tests/templates/790ExpungementTemplate_usingythongvars.docx", 'rb') as tp:
            expungementTemplate.create(name="Expungement Petition Template", data=tb.read(), doctype="docx")

    def test_petition_template(self):
        """  A petition template has a doctype"""
        expungement_template = PetitionTemplate.objects.get(name="Expungement Petition Template")
        self.assertEqual(expungement_template.doctype, "docx")

