"""Django models related to the large frontpage-application."""
from django.db import models


class User(models.Model):
    """Base model for all information related to single user"""
    user_id = models.CharField(max_length=22, primary_key=True)
    # Neither of these used because of time constraints
    majorcode = models.CharField(max_length=15)
    minorcode = models.CharField(max_length=15)

    def __unicode__(self):
        return self.user_id


class PlannedCourse(models.Model):
    """Model containing users planned courses"""
    # Only course code is needed here, all other information is available
    # through API(tm)
    user_id = models.CharField(max_length=22)
    course_code = models.CharField(max_length=20)

    def __unicode__(self):
        return self.course_code + "/" + self.user_id
