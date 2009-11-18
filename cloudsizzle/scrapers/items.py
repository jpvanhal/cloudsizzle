# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose, Join

class ItemLoader(XPathItemLoader):
    default_output_processor = Compose(Join(), unicode.strip)

class FacultyItem(Item):
    name = Field()

class DepartmentItem(Item):
    code = Field()
    name = Field()
    faculty = Field()

class CourseItem(Item):
    code = Field()
    name = Field()
    department = Field()
    credits = Field()
    teaching_period = Field()
    learning_outcomes = Field()
    content = Field()
    prerequisites = Field()
