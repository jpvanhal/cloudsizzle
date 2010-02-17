'''
Created on Feb 14, 2010

@author: pb
'''

from django.core.urlresolvers import reverse
from studyplanner.events.models import *
import api

class EventLog:

    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', object_scr='', update_time=''):
        self.img_scr=img_scr
        self.user_name=user_name
        self.user_scr=user_scr
        self.action=action
        self.object_name=object_name
        self.object_scr=object_scr
        self.update_time=update_time
    @classmethod
    def constructor(cls, user_ids):
        if user_ids == []:
            return []
        events = Event.objects.filter(user_id=user_ids).order_by('-time')[0:10]
        if not isinstance(user_ids, list):
            return cls.builder(user_id=user_ids, events=events)
        elif len(user_ids)==1:
            return cls.builder(user_id=user_ids[0], events=events)
        else:
            result = [] 
            for event in events:
                result.extend(cls.builder(event.user_id, events=[event,]))
            return result
        
    @classmethod
    def builder(cls, user_id, events):
        feeds = []
        from cloudsizzle.settings import ASI_BASE_URL
        img_scr = ASI_BASE_URL+ '/people/' + user_id + '/@avatar'
        user_scr = reverse('profile', args=[user_id])        
        user_inf = dict(api.people.get(user_id))
        try:
            user_name = user_inf['username']
        except (KeyError, TypeError):
            user_name = 'Unknown'

        if len(events) is 0:
            return []
        for event in events:         
             
            update_time = event.time
            if hasattr(event, 'plannedcourse'):
                course_code = event.plannedcourse.course_code
                object_name = course_code
                action = 'enrolled to'
                feeds.append(PlanCourseEventLog(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time, object_id=course_code))
            if hasattr(event, 'newfriendevent'):
                friend_id = event.newfriendevent.new_friend
                friend_inf = dict(api.people.get(friend_id))
                try:
                    friend_name = friend_inf['username']
                except (KeyError, TypeError):
                    friend_name = 'Unknown'
                object_name = friend_name
                action = 'became a friend of'
                feeds.append(NewFriendEventLog(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time, object_id=friend_id))
        return feeds
    
    def _get_object_scr(self, object_name):
        return ''


class PlanCourseEventLog(EventLog):
                
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time='', object_id=''):
        self.course_name = object_name+' '
        object_scr = self._get_object_scr(object_id)       
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=self.course_name, object_scr=object_scr, update_time=update_time)    
    def _get_object_scr(self, object_id):
        courseinfo = api.course.get_course(object_id)
        self.course_name += courseinfo['name']        
        return reverse('show_course', args=[courseinfo['faculty'], courseinfo['department'], courseinfo['code']])
class NewFriendEventLog(EventLog):
    
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time='', object_id=''):
        object_scr = self._get_object_scr(object_id)      
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)   
    def _get_object_scr(self, object_id):        
        return reverse('profile', args=[object_id])
             
   
        
if __name__ =='__main__':
    
    p1 = NewFriendEvent(user_id="bHC0t6gwur37J8aaWPEYjL", new_friend='a0cHdkgvSr35qmaaWPEYjL')
    #p1.save()
    p2 = PlannedCourse(user_id="bHC0t6gwur37J8aaWPEYjL",course_code='A-8.2310')
    p2.save()
    #a = event(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb',user_scr='', action="like", object_name='miao', object_scr='http://dict.cn/')


