from rest_framework import serializers as S
from .models import ChargeRecord

class ChargeRecordSerializer(S.ModelSerializer):
    class Meta:
        model = ChargeRecord
        fields = '__all__'

    grade = S.CharField(required=False)