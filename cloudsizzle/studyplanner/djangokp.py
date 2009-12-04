import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'

from kpwrapper import SIBConnection, Triple
from courselist.models import Course, Faculty, Department

faculty_map = {}
department_map = {}

#query the course codes
with SIBConnection('SIB console', 'preconfigured') as sc:
    faculties = sc.query(Triple(None, 'rdf:type', 'Faculty'))
    for triple in faculties:
        faculty = Faculty(code=triple.subject)
        for attr in ('name', ):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                setattr(faculty, attr, str(attr_triple.object))
            except IndexError:
                pass
        faculty.slug = faculty.code.lower()
        faculty.save()
        faculty_map[str(triple.subject)] = faculty

    departments = sc.query(Triple(None, 'rdf:type', 'Department'))
    for triple in departments:
        department = Department(code=triple.subject)
        for attr in ('name', ):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                setattr(department, attr, str(attr_triple.object))
            except IndexError:
                pass
        faculty_triple = sc.query(Triple(triple.subject, 'faculty', None))[0]
        department.faculty = faculty_map[str(faculty_triple.object)]
        department.slug = department.code.lower()
        department.save()
        department_map[str(triple.subject)] = department

    courses = sc.query(Triple(None, 'rdf:type', 'Course'))
    for triple in courses:
        course = Course(code=triple.subject)
        for attr in ('name', 'extent', 'content', 'teaching_period', 'learning_outcomes', 'prerequisites', 'study_materials'):
            try:
                attr_triple = sc.query(Triple(triple.subject, attr, None))[0]
                setattr(course, attr, str(attr_triple.object))
            except IndexError:
                print e
                print triple.subject, attr
            except UnicodeEncodeError, e:
                print e
                print triple.subject, attr
        department_triple = sc.query(Triple(triple.subject, 'department', None))
        course.slug = course.code.lower()
        course.faculty = department_map[str(department_triple.object)]
        course.save()
