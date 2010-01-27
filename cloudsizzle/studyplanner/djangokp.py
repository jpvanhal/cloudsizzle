import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'cloudsizzle.studyplanner.settings'
from django.contrib.auth.models import User
from cloudsizzle.kp import SIBConnection, Triple
from courselist.models import Course, Faculty, Department
from completedstudies.models import CompletedCourse

def populate_object(obj, subject, allowed_predicates):
    triples = sc.query(Triple(subject, None, None))
    for triple in triples:
        if str(triple.predicate) in allowed_predicates:
            setattr(obj, str(triple.predicate), unicode(triple.object))

faculty_map = {}
department_map = {}

#query the course codes
with SIBConnection('SIB console', 'preconfigured') as sc:
    faculties = sc.query(Triple(None, 'rdf:type', 'Faculty'))
    for triple in faculties:
        faculty = Faculty(code=triple.subject)
        populate_object(faculty, triple.subject, ['name'])
        faculty.slug = faculty.code.lower()
        faculty.save()
        faculty_map[str(triple.subject)] = faculty

    departments = sc.query(Triple(None, 'rdf:type', 'Department'))
    for triple in departments:
        department = Department(code=triple.subject)
        populate_object(department, triple.subject, ['name'])
        faculty_triple = sc.query(Triple(triple.subject, 'faculty', None))[0]
        department.faculty = faculty_map[str(faculty_triple.object)]
        department.slug = department.code.lower()
        department.save()
        department_map[str(triple.subject)] = department

    courses = sc.query(Triple(None, 'rdf:type', 'Course'))
    for triple in courses:
        course = Course(code=triple.subject)
        populate_object(course, triple.subject, ['name', 'extent', 'content', 'teaching_period', 'learning_outcomes', 'prerequisites', 'study_materials'])
        department_triple = sc.query(Triple(triple.subject, 'department', None))[0]
        course.slug = course.code.lower()
        course.department = department_map[str(department_triple.object)]
        course.save()

    completedcr = sc.query(Triple(None, 'has_completed', None))
    for triple in completedcr:
        username = triple.subject
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User(username=username)
            user.save()
        course = CompletedCourse()
        course.student = user
        populate_object(course, triple.object, ['code', 'name', 'cr', 'ocr', 'grade', 'date', 'teacher'])
        course.save()
