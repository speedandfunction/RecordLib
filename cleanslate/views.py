"""
Views for the Recordlib webapp.

"""

import logging
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import permissions, status
from RecordLib.crecord import CRecord
from RecordLib.sourcerecords import SourceRecord as RLSourceRecord
from RecordLib.analysis import Analysis
from RecordLib.utilities.serializers import to_serializable
from RecordLib.analysis.ruledefs import (
    expunge_summary_convictions,
    expunge_nonconvictions,
    expunge_deceased,
    expunge_over_70,
    seal_convictions,
)
from RecordLib.petitions import Expungement, Sealing
from .serializers import (
    CRecordSerializer,
    DocumentRenderSerializer,
    FileUploadSerializer,
    UserProfileSerializer,
    UserSerializer,
    IntegrateSourcesSerializer,
    SourceRecordSerializer,
    DownloadDocsSerializer,
)
from .compressor import Compressor
from .services import download
from .models import SourceRecord

logger = logging.getLogger(__name__)


class FileUploadView(APIView):
    """
    Handle uploads of source records.
    """

    parser_classes = [MultiPartParser, FormParser]

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """Accept dockets and summaries locally uploaded by a user, save them to the server,
        and return SourceRecords relating to those files..


        This POST needs to be a FORM post, not a json post.
        """
        file_serializer = FileUploadSerializer(data=request.data)
        if file_serializer.is_valid():
            files = file_serializer.validated_data.get("files")
            results = []
            try:
                for upload in files:
                    source_record = SourceRecord.from_unknown_file(
                        upload, owner=request.user
                    )
                    source_record.save()
                    if source_record is not None:
                        results.append(source_record)
                        # TODO FileUploadView should report errors in turning uploaded pdfs into SourceRecords.
                return Response(
                    {"source_records": SourceRecordSerializer(results, many=True).data},
                    status=status.HTTP_200_OK,
                )
            except Exception as err:
                return Response(
                    {"error_message": f"Parsing failed: {str(err)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error_message": "Invalid Data.", "errors": file_serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SourceRecordsFetchView(APIView):
    """
    Views for handling fetching source records that are sent as urls
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        API endpoint that takes a set of cases with urls to docket or summary sheets, downloads them,
        and returns SourceRecords, which point to the documents' ids in the database.

        This is for accepting the UJS Search results, and creating SourceRecord objects describing each of those search results. 
        
        This view does _not_ attempt download the source records, or parse them.

        """
        try:
            posted_data = DownloadDocsSerializer(data=request.data)
            if posted_data.is_valid():
                records = posted_data.save(owner=request.user)
                download.source_records(records)
                return Response(
                    DownloadDocsSerializer({"source_records": records}).data,
                )
            return Response({"errors": posted_data.errors})
        except Exception as err:
            return Response({"errors": [str(err)]})


class IntegrateCRecordWithSources(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        """
        Accept a CRecord and a set of SourceRecords.
        
        Parse the SourceRecords, and incorporate the information that the SourceRecords
        contain into the CRecord.

        Two api endpoints of the Django app interact with RecordLib. This one
        accepts a serialzed crecord and a list of sourcerecords. It attempts
        to parse each source_record, and then integrate the sourcerecords into the crecord.

        TODO IntegrateCRecordWithSources should communicate failures better.

        """
        try:
            serializer = IntegrateSourcesSerializer(data=request.data)
            if serializer.is_valid():
                nonfatal_errors = []
                crecord = CRecord.from_dict(serializer.validated_data["crecord"])
                source_records = []
                for source_record_data in serializer.validated_data["source_records"]:
                    try:
                        source_records.append(
                            SourceRecord.objects.get(id=source_record_data["id"])
                        )
                    except Exception:
                        pass

                for source_record in source_records:
                    try:
                        rlsource = RLSourceRecord(
                            source_record.file.path, parser=source_record.get_parser()
                        )
                        source_record.parse_status = SourceRecord.ParseStatuses.SUCCESS
                        crecord.add_sourcerecord(
                            rlsource,
                            case_merge_strategy="overwrite_old",
                            override_person=True,
                        )
                    except Exception:
                        source_record.parse_status = SourceRecord.ParseStatuses.FAILURE
                        nonfatal_errors.append(
                            f"Could not parse {source_record.docket_num} ({source_record.record_type})"
                        )
                    finally:
                        source_record.save()
                return Response(
                    {
                        "crecord": CRecordSerializer(crecord).data,
                        "source_records": SourceRecordSerializer(
                            source_records, many=True
                        ).data,
                        "errors": nonfatal_errors,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as err:
            return Response(
                {"errors": [str(err)]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AnalysisView(APIView):
    """
    Views related to an analysis of a CRecord.
    """

    # noinspection PyMethodMayBeStatic
    def post(self, request):
        """ Analyze a Criminal Record for expungeable and sealable cases and charges.
        
        POST body should be json-endoded CRecord object. 

        Return, if not an error, will be a json-encoded Decision that explains the expungements
        and sealings that can be generated for this record.

        """
        try:
            serializer = CRecordSerializer(data=request.data)
            if serializer.is_valid():
                rec = CRecord.from_dict(serializer.validated_data)
                analysis = (
                    Analysis(rec)
                    .rule(expunge_deceased)
                    .rule(expunge_over_70)
                    .rule(expunge_nonconvictions)
                    .rule(expunge_summary_convictions)
                    .rule(seal_convictions)
                )
                return Response(to_serializable(analysis))
            return Response(
                {"validation_errors": serializer.errors},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as err:
            logger.error(err)
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class RenderDocumentsView(APIView):
    """ Create pettions and an Overview document from an Analysis.
    
    POST should be a json-encoded object with an 'petitions' property that is a list of
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Accept an object describing petitions to generate, and generate them.
        """
        try:
            serializer = DocumentRenderSerializer(data=request.data)
            if serializer.is_valid():
                petitions = []
                for petition_data in serializer.validated_data["petitions"]:
                    if petition_data["petition_type"] == "Sealing":
                        new_petition = Sealing.from_dict(petition_data)
                        # this could be done earlier, if needed, to avoid querying db over and over.
                        # but we'd need to test what types of templates are actually needed.
                        try:
                            new_petition.set_template(
                                request.user.userprofile.sealing_petition_template.file
                            )
                            petitions.append(new_petition)
                        except Exception as err:
                            logger.error(
                                "User has not set a sealing petition template, or "
                            )
                            logger.error(str(err))
                            continue
                    else:
                        new_petition = Expungement.from_dict(petition_data)
                        try:
                            new_petition.set_template(
                                request.user.userprofile.expungement_petition_template.file
                            )
                            petitions.append(new_petition)
                        except Exception as err:
                            logger.error(
                                "User has not set an expungement petition template, or "
                            )
                            logger.error(str(err))
                            continue
                client_last = petitions[0].client.last_name
                petitions = [(p.file_name(), p.render()) for p in petitions]
                package = Compressor(f"ExpungementsFor{client_last}.zip", petitions)

                logger.info("Returning x-accel-redirect to zip file.")

                resp = HttpResponse()
                resp["Content-Type"] = "application/zip"
                resp["Content-Disposition"] = f"attachment; filename={package.name}"
                resp["X-Accel-Redirect"] = f"/protected/{package.name}"
                return resp
            else:
                raise ValueError
        except Exception as e:
            logger.error(str(e))
            return Response("Something went wrong", status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "user": UserSerializer(request.user).data,
                "profile": UserProfileSerializer(request.user).data,
            }
        )

