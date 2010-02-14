"""Utility functions related to courses"""

from studyplanner.frontpage.models import PlannedCourse
from django.db.models import Q
import api


def friends_taking_course(user_id, course_code):
    """Get friends taking a specific course

    Arguments:
    user_id --- ASI user ID for the person whose friends will
                be searched through. Case sensitive
    course_code -- Course code for the course being counted.
                   Case sensitive
    
    """
    friends = api.people.get_friends(user_id)
    # How do I split this line?
    friends_on_course = PlannedCourse.objects.filter(user_id__in=friends, course_code=course_code).values_list('user_id', flat=True)
                                                    
    return friends_on_course

def count_friends_taking_course(user_id, course_code):
    """Count friends taking a specific course
    
    Arguments:
    user_id --- ASI user ID for the person whose friends will
                be searched through. Case sensitive
    course_code -- Course code for the course being counted.
                   Case sensitive
    
    """
    friends = api.people.get_friends(user_id)
    # This needs splitting too.
    count_of_friends = PlannedCourse.objects.filter(user_id__in=friends, course_code=course_code).count()
    
    return count_of_friends
    