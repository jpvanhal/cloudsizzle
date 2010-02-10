from django.db import models
from cloudsizzle import api

# Create your models here.

class Event(models.Model):
    user_id = models.CharField(max_length=22)
    time = models.DateTimeField(auto_now_add=True)

class PlannedCourse(Event):
    course_code = models.CharField(max_length=30)
    
class FriendRequest(Event):
    new_friend = models.CharField(max_length=22)

class NewFriendEvent(Event):
    new_friend = models.CharField(max_length=22)
