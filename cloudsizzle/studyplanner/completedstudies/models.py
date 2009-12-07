from django.db import models

from django.contrib.auth.models import User
# Create your models here.


class CompletedCourse(models.Model):
    """
    Model for completed studies
    """
    student = models.ForeignKey(User, related_name='completed_courses')
    code = models.CharField(max_length=11)
    name = models.CharField(max_length=100)
    cr = models.IntegerField(null=True)
    ocr = models.IntegerField(null=True)
    grade = models.CharField(max_length=5)
    date = models.DateField()
    teacher = models.CharField(max_length=60)

class Teacher(models.Model):
    """
    should be updated for the teachers to combine them with course information
    """
    name = models.CharField(max_length = 30)
