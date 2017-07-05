# Scrapy settings for TheHindu project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'TheHindu'

SPIDER_MODULES = ['TheHindu.spiders']
NEWSPIDER_MODULE = 'TheHindu.spiders'

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline',]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'news'
MONGODB_COLLECTION = 'thehindu'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'TheHindu (+http://www.yourdomain.com)'
