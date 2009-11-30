from kpwrapper import SIBConnection, Triple
from cloudsizzle.studyplanner.courselist.models import Course

#query the course codes
with SIBConnection('SIB console', 'preconfigured') as sc:
    results = sc.query(Triple(None, 'rdf:type', 'Course'))
    for tr in results:
        cc = tr.subject
        cn = tr.object
        print(cc)
        c = Course(course_code=cc, course_name=cn)
        c.save()

