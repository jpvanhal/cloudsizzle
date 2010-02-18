"""
Scrapy settings

For simplicity, this file contains only the most important settings by
default. All the other settings are documented here:

     http://doc.scrapy.org/topics/settings.html

Or you can copy and paste them from where they're defined in Scrapy:

     scrapy/conf/default_settings.py

"""
BOT_NAME = 'cloudsizzle'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['cloudsizzle.scrapers.noppa.spiders']
NEWSPIDER_MODULE = 'cloudsizzle.scrapers.noppa.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

LOG_LEVEL = 'DEBUG'

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': None
}

ITEM_PIPELINES = [
    'cloudsizzle.scrapers.noppa.pipelines.SIBPipeline',
]
