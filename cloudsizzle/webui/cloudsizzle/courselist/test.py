# Create your views here.
from kpwrapper import SIBConnection, Triple

def index(request):
    sc = SIBConnection('SIB console', 'preconfigured')
    print("query")
    results = sc.query(Triple(None, None, None))
    print("got results")
    for triple in results:
        print(triple)
    print("printed results")
    
    sc.close()
    
    #print(ret)
    #return ret
    
    
index(None)
