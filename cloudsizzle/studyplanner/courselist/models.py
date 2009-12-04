from django.db import models

# Create your models here.

class Course(models.Model):
    slug = models.SlugField()
    code = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    extent = models.CharField(max_length=5)
    teaching_period = models.CharField(max_length=20)
    learning_outcomes = models.TextField()
    content = models.TextField()
    prerequisites = models.TextField()
    study_materials = models.TextField()
    department = models.ForeignKey('Department', related_name='courses')

    def __unicode__(self):
        return '{0} {1}'.format(self.code, self.name)

class Faculty(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    slug = models.SlugField()
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Department(models.Model):
    slug = models.SlugField()
    code = models.CharField(max_length=11, primary_key=True)
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='departments')

    def __unicode__(self):
        return '{0} {1}'.format(self.code, self.name)
