from django.urls import path
from .views import *

urlpatterns = [
    path('', ChargeRecordList.as_view()),
    path('guess/', GuessChargeGrade.as_view()),
]
