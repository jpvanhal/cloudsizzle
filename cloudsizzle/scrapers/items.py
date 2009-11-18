# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import Identity
from scrapy.contrib.loader import XPathItemLoader
from scrapy.contrib.loader.processor import MapCompose, Join, Identity
from scrapy.utils.markup import replace_tags, remove_entities
from cloudsizzle.scrapers.utils import remove_extra_whitespace

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

class CourseOverviewItem(Item):
    course = Field()
    credits = Field()
    teaching_period = Field()
    learning_outcomes = Field()
    content = Field()
    prerequisites = Field()

class ItemLoader(XPathItemLoader):
    default_input_processor = MapCompose(
        lambda text: replace_tags(text, ' '), 
        remove_entities, 
        unicode.strip,
        remove_extra_whitespace
    )
    default_output_processor = Join()

