"""
The models for scraped items.

See documentation in:

http://doc.scrapy.org/topics/items.html

"""
from scrapy.item import Item, Field


class FacultyItem(Item):
    code = Field()
    name = Field()


class DepartmentItem(Item):
    code = Field()
    name = Field()
    faculty = Field()


class CourseItem(Item):
    code = Field()
    name = Field()
    department = Field()


class CourseOverviewItem(Item):
    course = Field()
    extent = Field()
    teaching_period = Field()
    learning_outcomes = Field()
    content = Field()
    prerequisites = Field()
    study_materials = Field()
