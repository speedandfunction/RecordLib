import logging
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import ChargeRecord
from .serializers import ChargeRecordSerializer
from .services import guess_grade

logger = logging.getLogger(__name__)



class ChargeRecordList(generics.ListCreateAPIView):
    queryset = ChargeRecord.objects.all()
    serializer_class = ChargeRecordSerializer
    permission_classes = [IsAdminUser]


class GuessChargeGrade(generics.RetrieveAPIView):
    queryset = ChargeRecord.objects.all()
    serializer_class = ChargeRecordSerializer
    permission_classes = []

    def get(self, request):
        """
        Guess the grade of a charge sent as query params. 

        N.B. Since these are necessarily guesses, don't save the results to the database.
        """
        crSerializer = ChargeRecordSerializer(data = request.query_params)
        if crSerializer.is_valid():
            cr = ChargeRecord(**crSerializer.validated_data)
            return Response(guess_grade(cr, self.queryset.all()), status=status.HTTP_200_OK)
        else:
            return Response({"errors": crSerializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        


