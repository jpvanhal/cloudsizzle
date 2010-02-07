from cloudsizzle.asi.service import ASIServiceKnowledgeProcessor
from cloudsizzle.asi.client import LoginClient, LogoutClient
from cloudsizzle.kp import SIBConnection

ASI_CLIENT = None

def start():
    global ASI_CLIENT

    sc = SIBConnection('ASI service client', method='preconfigured')
    sc.open()

    ASI_CLIENT = ASIServiceKnowledgeProcessor(services=(
       LoginClient(sc),
       LogoutClient(sc),
    ))
    ASI_CLIENT.start()

def stop():
    ASI_CLIENT.stop()

start()
