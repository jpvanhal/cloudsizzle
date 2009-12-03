from django.db import models

# Create your models here.

class Course(models.Model):
    code = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    extent = models.CharField(max_length=5)
    teaching_period = models.CharField(max_length=20)
    learning_outcomes = models.TextField()
    content = models.TextField()
    prerequisites = models.TextField()
    study_materials = models.TextField()
    department = models.ForeignKey('Department')
    
class Faculty(models.Model):
    code = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    
class Department(models.Model):
    code = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty')

