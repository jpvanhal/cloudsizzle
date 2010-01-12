# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html
import datetime
from scrapy.item import Field
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

class ItemLoader(XPathItemLoader):
    default_input_processor = MapCompose(
        lambda text: replace_tags(text, ' '),
        remove_entities,
        unicode.strip,
        remove_extra_whitespace
    )
    default_output_processor = Join()
