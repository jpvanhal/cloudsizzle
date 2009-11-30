# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import datetime
from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import Compose, MapCompose, Join, Identity, TakeFirst
from scrapy.utils.markup import replace_tags, remove_entities
from cloudsizzle.scrapers.utils import remove_extra_whitespace

class DateField(Field):
    def __init__(self, date_format):
        def date_from_string(text):
            return datetime.datetime.strptime(text, date_format).date()
        super(DateField, self).__init__(
            output_processor=Compose(TakeFirst(), date_from_string))

class FacultyItem(Item):
    id = Field()
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

class CompletedCourseItem(Item):
    name = Field()
    code = Field()
    cr = Field()
    ocr = Field()
    grade = Field()
    date = DateField('%d.%m.%Y')
    teacher = Field()
    module = Field()

class ModuleItem(Item):
    name = Field()
    code = Field()

class ItemLoader(XPathItemLoader):
    default_input_processor = MapCompose(
        lambda text: replace_tags(text, ' '),
        remove_entities,
        unicode.strip,
        remove_extra_whitespace
    )
    default_output_processor = Join()
