from __future__ import annotations
from django.db import models
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save
import io
import uuid
from typing import Optional
from dataclasses import dataclass, asdict
import re
from RecordLib.sourcerecords.docket.re_parse_pdf import (
    re_parse_pdf as docket_pdf_parser,
)
from RecordLib.sourcerecords.summary.parse_pdf import parse_pdf as summary_pdf_parser


class DocumentTemplate(models.Model):
    """Abstact model for storing a template for expungement or sealing petitions."""

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="templates/")
    default = models.BooleanField(null=True)

    class Meta:
        abstract = True


class ExpungementPetitionTemplate(DocumentTemplate):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["default"],
                condition=models.Q(default=True),
                name="unique_default_expungement_petition",
            )
        ]

    pass


class SealingPetitionTemplate(DocumentTemplate):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["default"],
                condition=models.Q(default=True),
                name="unique_default_sealing_petition",
            )
        ]

    pass


class UserProfile(models.Model):
    """Information unrelated to authentication that is relevant to a user. """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    expungement_petition_template = models.ForeignKey(
        ExpungementPetitionTemplate,
        on_delete=models.CASCADE,
        null=True,
        related_name="expugement_template_user_profiles",
    )
    sealing_petition_template = models.ForeignKey(
        SealingPetitionTemplate,
        on_delete=models.CASCADE,
        null=True,
        related_name="sealing_petition_template_user_profiles",
    )


def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)


def set_default_templates(sender, **kwargs):
    """ 
    Set the default templates to a new user's templates, 
    If the user hasn't picked any templates, and if there are 
    default templates in the database.
    """
    profile = kwargs["instance"]
    if kwargs["created"]:
        if (
            profile.expungement_petition_template is None
            and ExpungementPetitionTemplate.objects.filter(default__exact=True).count()
            == 1
        ):
            profile.expungement_petition_template = ExpungementPetitionTemplate.objects.filter(
                default__exact=True
            ).all()[
                0
            ]
        if (
            profile.sealing_petition_template is None
            and SealingPetitionTemplate.objects.filter(default__exact=True).count() == 1
        ):
            profile.sealing_petition_template = SealingPetitionTemplate.objects.filter(
                default__exact=True
            ).all()[0]

        profile.save()


post_save.connect(set_default_templates, sender=UserProfile)


@dataclass
class SourceRecordFileInfo:
    caption: str = ""
    docket_num: str = ""
    court: str = ""
    url: str = ""
    record_type: str = ""
    fetch_status: str = ""


def source_record_info(filename: str):
    """
    TODO what is this method for?
    """
    file_info = SourceRecordFileInfo()
    if re.search("pdf$", filename, re.IGNORECASE):
        if re.search("summary", filename, re.IGNORECASE):
            file_info.record_type = SourceRecord.RecTypes.SUMMARY_PDF
        elif re.search("docket", filename, re.IGNORECASE):
            file_info.record_type = SourceRecord.RecTypes.DOCKET_PDF

        if re.search("CP", filename):
            file_info.court = SourceRecord.Courts.CP
        elif re.search("MD", filename):
            file_info.court = SourceRecord.Courts.MDJ

        file_info.fetch_status = SourceRecord.FetchStatuses.FETCHED
        return file_info
    else:
        return None


class SourceRecord(models.Model):
    """
    Class to manage documents that provide information about a person's criminal record, such as a 
    summary pdf sheet or a docket pdf sheet.
    
    caption="Comm. v. Smith",
        docket_num="CP-1234", 
        court=SourceRecord.COURTS.CP,
        url="https://ujsportal.gov", 
        record_type=SourceRecord.RecTypes.SUMMARY,
        owner=admin_user
    """

    @classmethod
    def from_unknown_file(
        cls, a_file: InMemoryUploadedFile, **kwargs
    ) -> Optional[SourceRecord]:
        """ Create a SourceRecord from an uploaded file, or return None if we cannot tell what the file is. """
        try:
            file_info = source_record_info(a_file.name)
            if file_info:
                return cls(**asdict(file_info), file=a_file, **kwargs)
            else:
                return None
        except:
            return None

    class Courts:
        """ Documents may come from one of these courts. """

        CP = "CP"
        MDJ = "MDJ"
        __choices__ = [
            ("CP", "CP"),
            ("MDJ", "MDJ"),
        ]

    class RecTypes:
        """ These types of records may be stored in this class. 
        """

        SUMMARY_PDF = "SUMMARY_PDF"
        DOCKET_PDF = "DOCKET_PDF"
        __choices__ = [
            ("SUMMARY_PDF", "SUMMARY_PDF"),
            ("DOCKET_PDF", "DOCKET_PDF"),
        ]

    def get_parser(self):
        """

        Based on the record_type of this SourceRecord, identify the parser it should use.
        """
        return {
            "SUMMARY_PDF": summary_pdf_parser,
            "DOCKET_PDF": docket_pdf_parser,
        }.get(self.record_type)

    class FetchStatuses:
        """
        Documents have to be fetched and saved locally. 
        Has a particular document been fetched?
        """

        NOT_FETCHED = "NOT_FETCHED"
        FETCHING = "FETCHING"
        FETCHED = "FETCHED"
        FETCH_FAILED = "FETCH_FAILED"
        __choices__ = [
            ("NOT_FETCHED", "NOT_FETCHED"),
            ("FETCHING", "FETCHING"),
            ("FETCHED", "FETCHED"),
            ("FETCH_FAILED", "FETCH_FAILED"),
        ]

    class ParseStatuses:
        """
        Track whether the source record could be successfully parsed or not.
        """

        UNKNOWN = "UNKNOWN"
        SUCCESS = "SUCESSFULLY_PARSED"
        FAILURE = "PARSE_FAILED"
        __choices__ = [
            ("UNKNOWN", "UNKNOWN"),
            ("SUCCESSFULLY_PARSED", "SUCCESSFULLY_PARSED"),
            ("PARSE_FAILED", "PARSE_FAILED"),
        ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    caption = models.CharField(blank=True, max_length=300)

    docket_num = models.CharField(blank=True, max_length=50)

    court = models.CharField(max_length=3, choices=Courts.__choices__, blank=True)

    url = models.URLField(blank=True, default="")

    record_type = models.CharField(
        max_length=30, blank=True, choices=RecTypes.__choices__
    )

    fetch_status = models.CharField(
        max_length=100,
        choices=FetchStatuses.__choices__,
        default=FetchStatuses.NOT_FETCHED,
    )

    parse_status = models.CharField(
        max_length=100,
        choices=ParseStatuses.__choices__,
        default=ParseStatuses.UNKNOWN,
    )

    file = models.FileField(null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
