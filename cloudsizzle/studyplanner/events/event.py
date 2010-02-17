'''
Created on Feb 14, 2010

@author: pb
'''

from django.core.urlresolvers import reverse
from studyplanner.events.models import *
import api

class event:
#class EventLog:

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
        events = Event.objects.filter(user_id=user_ids).order_by('-time')[0:10]
        return events
        '''
        if not isinstance(user_ids, list):
            return cls.builder(user_id=user_ids, events)
        elif len(user_ids)==1:
            return cls.builder(user_id=user_ids[0], events)
        elif len(user_ids)==0:
            return []
        else:
            result = [] 
            for event in events:
                result.extend(cls.builder(event.user_id, [event]))
            return result
        '''
    @classmethod
    def builder(cls, user_id, events):
        feeds = []
        from cloudsizzle.settings import ASI_BASE_URL
        img_scr = ASI_BASE_URL + user_id
        user_scr = reverse('profile', args=[user_id])
        
        user_inf = dict(api.people.get(user_id))
        try:
            user_name = user_inf['username']
        except (KeyError, TypeError):
            user_name = 'Unknown'
                
        
        if len(events) is 0:
            return []
        for event in events:
            
            object_name = event.object 
            update_time = event.time
            if hasattr(event, 'plannedcourse'):
                action = 'enrolled to'
                feeds.append(plan_course_event(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time))
            if hasattr(event, 'newfriendevent'):
                action = 'became a friend of'
                feeds.append(new_friend_event(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time))
        return feeds
    
    def get_object_scr(self, object_name):
        return ''


class plan_course_event(event):#EventLog):
                
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time=''):
        object_scr = self.get_object_scr(object_name)       
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)    
    def get_object_scr(self, object_name):
        courseinfo = api.course.get_course(object_name)
        object_name += courseinfo['name']        
        return reverse('show_course', args=[courseinfo['faculty'], courseinfo['department'], courseinfo['code']])
class new_friend_event(event):#EventLog):
    
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time=''):
        object_scr = self.get_object_scr(object_name)      
        EventLog.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)   
    def get_object_scr(self, object_name):        
        return reverse('profile', args=[object_name])
             
   
        
if __name__ =='__main__':
    p = FriendRequest(user_id="bHC0t6gwur37J8aaWPEYjL", new_friend='cwc2e4f14r362vaaWPEYjL')
    p1 = NewFriendEvent(user_id="cwc2e4f14r362vaaWPEYjL", new_friend='bHC0t6gwur37J8aaWPEYjL')
    #p1.save()
    a = event(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb',user_scr='', action="like", object_name='miao', object_scr='http://dict.cn/')
    b = event.constructor(user_ids="cwc2e4f14r362vaaWPEYjL")
    print len(b) 
    if isinstance(b, list):
        b = [b,]
    for b1 in b:
        print hasattr(b1, 'newfriendevent')


    print b[0].newfriendevent.new_friend
