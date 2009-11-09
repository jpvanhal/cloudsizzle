# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class CourseItem(Item):
    code = Field()
    name = Field()
    credits = Field()
    teaching_period = Field()
    learning_outcomes = Field()
    content = Field()
    prerequisites = Field()
