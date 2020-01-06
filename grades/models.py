from django.db import models

# Create your models here.
class ChargeRecord(models.Model):
    """
    A record indicating the grade of a charge, and how heavily that grade should be weighed
    when deciding how to predict the grade of a charge with a missing grade.


    """

    # Text describing the offense, as in "Eating loudly in library"
    offense = models.CharField(max_length=300)

    # Text identifying the title of the PA code violated, "18" in 
    # "18 Pa. Code 123 subsection A1".
    title = models.CharField(max_length=300)


    # Text identifying the section of the PA code violated, "123" in 
    # "18 Pa. Code 123 subsection A1".
    section = models.CharField(max_length=30)

    # Text identifying the subsection of the PA code violated, "A1" in 
    # "18 Pa. Code 123 subsection A1".
    subsection = models.CharField(max_length=30, default="")


    # Text identifying the grade of the offense, as in "M1" or "F2".
    grade = models.CharField(max_length=20)


    # Integer identifying how heavily the grade in this ChargeRecord should weigh,
    # when attempting to guess the grade of an ungraded charge. 
    weight = models.IntegerField(default=1)
