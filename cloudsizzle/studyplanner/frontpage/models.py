"""Django models related to the large frontpage-application."""
from django.db import models

# Create your models here.

"""Base model for all information related to single user"""
class User(models.Model):
    user_id = models.CharField(max_length=22)
    # Neither of these used because of time constraints
    majorcode = models.CharField(max_length=15)
    minorcode = models.CharField(max_length=15)

    def __unicode__(self):
        return self.user_id

"""Model containing users planned courses"""
class PlannedCourse(models.Model):
    # Only course code is needed here, all other information is available
    # through API(tm)
    user = models.ForeignKey(User)
    course_code = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.course_code 