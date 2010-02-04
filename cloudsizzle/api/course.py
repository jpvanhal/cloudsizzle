import time
from cloudsizzle import pool
from cloudsizzle.kp import Triple, bnode, uri, literal

# Also do these preserve unicode characters?

def search(query):
    """Search for courses whose course code or name contains the query string."""
    with pool.get_connection() as sc:    
        # This unfortunately must be done in Python. WQL could possibly help here
        # Of course SIB (or Python-KP) is slow as molasses anyway.
        query = query.lower()
        t1 = time.time()
        course_names = sc.query(Triple(None, uri('name'), None))
        t2 = time.time()
        course_codes = [str(course.subject) for course in course_names if query in course.subject.lower() or query in course.object.lower()] 
        t3 = time.time()
    
        print 'SIB took %0.3f ms' % ((t2-t1)*1000.0)
        print 'Python search took %0.3f ms' % ((t3-t2)*1000.0)
    
        return course_codes

def get_course(course_code):
    """Returns all information for course identified by course code."""
    # Need to find the course code with correct capitalization first
    course_code = search(course_code)[0]
    
    with pool.get_connection() as sc:    
        course_triples = sc.query(Triple(uri(course_code), None, None))
    
        courseinfo = {}
        for triple in course_triples:
            p, o = str(triple.predicate), str(triple.object)
            # filters out RDF meta information
            if "www.w3.org" not in p:
                courseinfo[p] = o
    
        return courseinfo

# This and the following are identical in structure. Probably a place for
# some abstraction
def get_courses_by_department(department_code):
    """Returns courses arranged by given department as identified
    by department code."""
    with pool.get_connection() as sc:
        course_ids = [x.subject for x in sc.query(Triple(None, None, uri(department_code.upper())))] 
        course_names = [sc.query(Triple(x, uri('name'), None))[0] for x in course_ids]

        return [{'code':str(x.subject), 'slug':str(x.subject).lower(), 'name':str(x.object)} for x in course_names]

def get_departments_by_faculty(faculty_code):
    with pool.get_connection() as sc:
        department_ids = [x.subject for x in sc.query(Triple(None, None, uri(faculty_code)))]
        department_names = [sc.query(Triple(x, uri('name'), None))[0] for x in department_ids]
        
        return ([{'slug': str(x.subject).lower(), 'code': str(x.subject), 'name': str(x.object)} for x in department_names])

def get_faculties():
    with pool.get_connection() as sc:
        # Get list of faculties with their ids
        faculties_ids = [x.subject for x in sc.query(Triple(None, "rdf:type", "Faculty"))]
        # Get id-name triplets by ids
        faculties = []
        for id in faculties_ids:
            faculty = sc.query(Triple(id, 'name', None))
            faculties.append({'slug': str(id), 'name': str(faculty[0].object)})
        # Final form is id-name dictionary
   
        return faculties
        