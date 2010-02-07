from cloudsizzle.asi.service import ASIServiceKnowledgeProcessor
from cloudsizzle.asi.client import LoginClient, LogoutClient
from cloudsizzle.kp import SIBConnection

ASI_CLIENT = None

def init():
    global ASI_CLIENT

    sc = SIBConnection('ASI service client', method='preconfigured')
    sc.open()

    ASI_CLIENT = ASIServiceKnowledgeProcessor(services=(
       LoginClient(sc),
       LogoutClient(sc),
    ))

def get_service(name):
    if not ASI_CLIENT:
        init()
    return ASI_CLIENT[name]
