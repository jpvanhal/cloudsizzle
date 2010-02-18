"""
The models for scraped items.

See documentation in:

http://doc.scrapy.org/topics/items.html

"""
from scrapy.item import Item, Field
from cloudsizzle.scrapers.items import DateField


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
