# Scrapy settings
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#
# Or you can copy and paste them from where they're defined in Scrapy:
#
#     scrapy/conf/default_settings.py
#

BOT_NAME = 'cloudsizzle'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['cloudsizzle.scrapers.spiders']
NEWSPIDER_MODULE = 'cloudsizzle.scrapers.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

ITEM_PIPELINES = [
    'cloudsizzle.scrapers.pipelines.UTF8Pipeline',
    'cloudsizzle.scrapers.pipelines.SIBPipeline',
]

LOG_LEVEL = 'INFO'
