# Scrapy settings for SportsKeeda project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'SportsKeeda'

SPIDER_MODULES = ['SportsKeeda.spiders']
NEWSPIDER_MODULE = 'SportsKeeda.spiders'

ITEM_PIPELINES = ['scrapy_mongodb.MongoDBPipeline',]

MONGODB_URI = 'mongodb://localhost:27017'
MONGODB_DATABASE = 'news'
MONGODB_COLLECTION = 'sportskeeda'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'SportsKeeda (+http://www.yourdomain.com)'
