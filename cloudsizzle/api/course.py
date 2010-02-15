"""Provides an API for fetching information about courses and their structures.

"""
from cloudsizzle import pool
from cloudsizzle.kp import Triple, uri
from cloudsizzle.utils import fetch_rdf_graph


def search(query):
    """Search for courses whose course code or name contains the query
    string. Search is case insensitive

    Arguments:
    query -- The query string. Please use unicode query string, if you want to
             have a case insensitive search for unicode characters also.

    """
    query = query.lower()
    if isinstance(query, unicode):
        query = query.encode('utf8')

    with pool.get_connection() as sc:
        # This unfortunately must be done in Python. WQL could possibly help
        # here. Of course SIB (or Python-KP) is slow as molasses anyway.

        # Get a list of valid course codes as also Faculties and Departments
        # have 'name' predicate.
        course_triples = sc.query(Triple(None, 'rdf:type', 'Course'))
        valid_courses = set(str(triple.subject) for triple in course_triples)

        name_triples = sc.query(Triple(None, 'name', None))

        course_codes = []
        for triple in name_triples:
            course_code = str(triple.subject)
            course_name = str(triple.object)
            if course_code not in valid_courses:
                continue
            if query in course_code.lower() or query in course_name.lower():
                course_codes.append(course_code)

        return sorted(course_codes)


def get_course(code):
    """Returns all information for course identified by course code. Search is
    case sensitive

    """
    with pool.get_connection() as sc:
        # Make sure there is a course with the given code
        triples = sc.query(Triple(code, "rdf:type", "Course"))
        if not triples:
            msg = 'There is no course with code "{0}".'.format(code)
            raise Exception(msg)

        
        course = fetch_rdf_graph(code, dont_follow=['department'])
        course['code'] = code

        # Fetch department and faculty codes separately, as the structure
        # constructed by fetch_rdf_graph becomes sanely does not
        # contain the codes. These just go and assume that every course
        # has both faculty and department. With Noppa scraping this
        # is necessarily true.
        triples = sc.query(Triple(course['code'], 'department', None))
        course['department'] = str(triples[0].object)
        
        triples = sc.query(Triple(course['department'], 'faculty', None))
        course['faculty'] = str(triples[0].object)

        return course

# This and the following are identical in structure. Probably a place for
# some abstraction


def get_courses_by_department(code):
    """Returns courses by given department as identified by department code.
    Department code is case sensitive

    """
    with pool.get_connection() as sc:
        triples = sc.query(Triple(None, 'department', uri(code)))
        course_codes = [str(triple.subject) for triple in triples]

        courses = []
        for course_code in course_codes:
            course = get_course(course_code)
            courses.append(course)

        # Sort the list of courses by their code
        return sorted(courses, key=lambda course: course['code'])


def get_departments_by_faculty(faculty_code):
    """Returns departments by a faculty.

    Arguments:
    faculty_code -- The code of the faculty whose departments are returned.
                    Faculty code is case sensitive.

    """
    with pool.get_connection() as sc:
        triples = sc.query(Triple(None, 'faculty', uri(faculty_code)))
        department_ids = [str(triple.subject) for triple in triples]

        departments = []
        for department_id in department_ids:
            department = get_department_info(department_id)
            departments.append(department)

        # Sort the list of departments by their code
        return sorted(departments, key=lambda department: department['code'])


def get_faculties():
    """Returns faculties listed in Noppa system ordered by their id."""
    with pool.get_connection() as sc:
        # Get list of faculties with their ids
        triples = sc.query(Triple(None, "rdf:type", "Faculty"))
        faculties_ids = [str(triple.subject) for triple in triples]

        # Get id-name triplets by ids
        faculties = []
        for faculty_id in faculties_ids:
            faculty = get_faculty_info(faculty_id)
            faculties.append(faculty)

        # Sort the list of faculties by their code
        return sorted(faculties, key=lambda faculty: faculty['code'])


def get_department_info(code):
    """Returns department info by the given department code.

    Arguments:
    code -- Case sensitive department code

    """
    with pool.get_connection() as sc:
        # Make sure there is a department with the given code
        triples = sc.query(Triple(code, "rdf:type", "Department"))
        if not triples:
            msg = 'There is no department with code "{0}".'.format(code)
            raise Exception(msg)

        name_triple = sc.query(Triple(code, 'name', None))
        department = {
            'code': code,
            'name': str(name_triple[0].object)
        }

        return department


def get_faculty_info(code):
    """Returns faculty info by the given faculty code.

    Arguments:
    code -- Faculty code as seen in Noppa's URL when viewing courses by
            faculty. This is case sensitive.

    """
    with pool.get_connection() as sc:
        # Make sure there is a faculty with the given code
        triples = sc.query(Triple(code, "rdf:type", "Faculty"))
        if not triples:
            msg = 'There is no faculty with code "{0}".'.format(code)
            raise Exception(msg)

        name_triple = sc.query(Triple(code, 'name', None))
        faculty = {
            'code': code,
            'name': str(name_triple[0].object)
        }
        return faculty
