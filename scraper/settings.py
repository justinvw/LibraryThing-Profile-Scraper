BOT_NAME = 'lt_profile_scraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)

