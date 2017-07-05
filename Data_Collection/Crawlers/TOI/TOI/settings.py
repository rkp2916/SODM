# Scrapy settings for TOI project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TOI'

SPIDER_MODULES = ['TOI.spiders']
NEWSPIDER_MODULE = 'TOI.spiders'

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline',]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'news'
MONGODB_COLLECTION = 'toi'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TOI (+http://www.yourdomain.com)'
