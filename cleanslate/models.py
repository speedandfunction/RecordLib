from django.db import models


class PetitionTemplate(models.Model):
    name = models.CharField(max_length=255)
    doctype = models.CharField(max_length=255)  # perhaps should be a reference table of supported types.
    data = models.BinaryField()