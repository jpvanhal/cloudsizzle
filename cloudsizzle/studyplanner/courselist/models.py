from django.db import models

# Create your models here.

class Course(models.Model):
    course_code = models.CharField(max_length=11, primary_key=True)
    course_name = models.CharField(max_length=100)
