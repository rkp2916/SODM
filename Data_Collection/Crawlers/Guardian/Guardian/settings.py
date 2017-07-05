# Scrapy settings for Guardian project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'Guardian'

SPIDER_MODULES = ['Guardian.spiders']
NEWSPIDER_MODULE = 'Guardian.spiders'

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline',]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'news'
MONGODB_COLLECTION = 'guardian'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'Guardian (+http://www.yourdomain.com)'
