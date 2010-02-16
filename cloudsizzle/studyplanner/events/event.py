'''
Created on Feb 14, 2010

@author: pb
'''
from django.core.urlresolvers import reverse

from studyplanner.events.models import EventsLog
import api

class event:

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
        events = EventsLog.object.filter(user_id=user_ids, action = action).order_by('time')[0:10]
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
                
        
        if not isinstance(events, list):
            events = [events,]
        for event in events:
            action = event.action
            object_name = event.object 
            update_time = event.time
            if action == 'enrolled to':
                feeds.append(plan_course_event(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time))
            if action == 'became a friend of':
                feeds.append(new_friend_event(img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                       action=action, object_name=object_name, update_time=update_time))
        return feeds
    
    def get_object_scr(self, object_name):
        return ''


class plan_course_event(event):
                
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time=''):
        object_scr = self.get_object_scr(object_name)       
        event.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)    

class new_friend_event(event):
    
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', update_time=''):
        object_scr = self.get_object_scr(object_name)      
        event.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)   
    def get_object_scr(self, object_name):        
        return reverse('profile', args=[object_name])
             
   
        
if __name__ =='__main__':
    a = event(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb',user_scr='', action="like", object_name='miao', object_scr='http://dict.cn/')
    pass