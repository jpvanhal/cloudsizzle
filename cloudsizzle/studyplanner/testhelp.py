from django.test.client import Client
from lxml import etree


def validate_html(url):
    """
    This function validates the html from the given url
    returns a tuple with boolean and a msg
    """
    #create the dtd
    parser = etree.XMLParser(dtd_validation=True,
                                 no_network=False,
                                 encoding='utf-8')

    #response from /
    c = Client()
    try:
        response = c.get(url)
    except:
        return
        
    result = True
    msg = ""
    try:
        vdoc = etree.fromstring(response.content,parser)
    except Exception as inst:
        result = False
        msg = str(inst)

    return (result,msg)
