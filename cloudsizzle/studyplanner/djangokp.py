from kpwrapper import SIBConnection, Triple
from courselist.models import Course
from courselist.models import Faculty
from courselist.models import Department

faculty_map = {}
department_map = {}

#query the course codes
with SIBConnection('SIB console', 'preconfigured') as sc:
    courses = sc.query(Triple(None, 'rdf:type', 'Course'))
    faculties = sc.query(Triple(None, 'rdf:type', 'Faculty'))
    departments = sc.query(Triple(None, 'rdf:type', 'Department'))
    for triple in faculties:
        faculty = Faculty(code=triple.subject)
        for attr in ('name', ):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                faculty.attr = attr_triple.subject
            except IndexError:
                pass
        faculty.save()
        faculty_map[triple.subject] = faculty
    for triple in departments:
        department = Department(code=triple.subject)
        for attr in ('name', ):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                department.attr = attr_triple.subject
            except IndexError:
                pass
        faculty_triple = sc.query(Triple(triple.subject, 'faculty', None))
        department.faculty = faculty_map[faculty_triple.object]  
        department.save()
        department_map[triple.subject] = department
    for triple in courses:
        course = Course(code=triple.subject)
        for attr in ('name', 'extent', 'content', 'teaching_period', 'learning_outcomes', 'prerequisites', 'study_materials'):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                course.attr = attr_triple.subject
            except IndexError:
                pass
        department_triple = sc.query(Triple(triple.subject, 'department', None))
        course.faculty = department_map[department_triple.object]
        course.save()

