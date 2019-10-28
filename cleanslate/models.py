from django.db import models
import io

class PetitionTemplate(models.Model):
    """Model for storing a docx template for expungement or sealing petitions."""
    
    name = models.CharField(max_length=255)
    doctype = models.CharField(max_length=255)  # perhaps should be a reference table of supported types.
    data = models.BinaryField()

    def data_as_bytesio(self):
        """
        DB stores `data` as bytes, but we more often want to use a BytesIO object.
        """
        return io.BytesIO(self.data)