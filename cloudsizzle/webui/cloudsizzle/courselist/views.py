# Create your views here.
from django.http import HttpResponse
from kpwrapper import SIBConnection, Triple

def index(request):
    html = ""
    with SIBConnection('SIB console', 'preconfigured') as sc:        
        results = sc.query(Triple(None, 'rdf:type', 'Course'))
        html = "<html><head><title>courselist</title></head><body><ul>"
        for triple in results:
            html += "<li>%s</li>" % triple.subject
        html += "</ul></body></html>"
    return HttpResponse(html)
