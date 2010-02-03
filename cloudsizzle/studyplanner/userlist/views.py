from django.http import HttpResponse
from django.template import Context, loader
import cloudsizzle.api as api


def list_users(request):
    """
    get a list of the users...
    
    just hear this should not be implemented...?
    """
    uids = api.people.get_all()
    users = []
    
    for uid in uids[:10]:
       users.append(uid)
       
       
    t = loader.get_template("userlist/list_of_users.html")
    c = Context({'users': users})
    
    return HttpResponse(t.render(c))
