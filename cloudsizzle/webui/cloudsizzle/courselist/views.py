# Create your views here.
from django.http import HttpResponse
from kpwrapper import SIBConnection, Triple

def index(request):
    sc = SIBConnection('SIB console', 'preconfigured')      
    results = sc.query(Triple(None, 'rdf:type', 'Course'))
    ret = [triple.object for triple in results]
    sc.close()
    return HttpResponse("hello")
