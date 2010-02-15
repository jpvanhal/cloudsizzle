from django.db import models

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
'''
#this action can be "'became a friend of'" for friend adding or
'enrolled to' for planing course. object should be friend_id or department_code#course_code
'''
class EventsLog(Event):
    action = models.CharField(max_length=40)
    object = models.CharField(max_length=30)
