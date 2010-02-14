'''
Created on Feb 14, 2010

@author: pb
'''
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
class plan_course_event(event):
    @classmethod
    def factory(cls, user_id, result_num):
        from cloudsizzle.settings import ASI_BASE_URL
        img_scr = ASI_BASE_URL + user_id
        user_scr = '../../profile/'+user_id
        
        user_inf = dict(api.people.get(user_id))
        try:
            user_name = user_inf['username']
        except (KeyError, TypeError):
            user_name = 'Unknown'
        
    def __init__(self, img_scr='', user_name='', user_scr='', action='', object_name='', object_scr='', update_time=''):       
        event.__init__(self, img_scr=img_scr, user_name=user_name, user_scr=user_scr,\
                   action=action, object_name=object_name, object_scr=object_scr, update_time=update_time)    
        
if __name__ =='__main__':
    a = event(img_scr='http://cos.alpha.sizl.org/people/bHC0t6gwur37J8aaWPEYjL/@avatar', user_name='pb',user_scr='', action="like", object_name='miao', object_scr='http://dict.cn/')
    pass
