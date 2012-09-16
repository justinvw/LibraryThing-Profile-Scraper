BOT_NAME = 'lt_profile_scraper'
BOT_VERSION = '1.0'

SPIDER_MODULES = ['scraper.spiders']
NEWSPIDER_MODULE = 'scraper.spiders'
ITEM_PIPELINES = ['scraper.pipelines.CSVExportPipeline']
USER_AGENT = '%s/%s' % (BOT_NAME, BOT_VERSION)
DOWNLOAD_DELAY = 1.0
RANDOMIZE_DOWNLOAD_DELAY = True
CONCURRENT_REQUESTS_PER_DOMAIN = 4

# Absolute path to the text that contains the inital list of LT profile
# URLs to crawl.
PROFILE_SEEDLIST = ''

# Absolute path to the directory where the crawl results should end up.
CSV_STORE_LOCATION = ''

# Wheter to follow and crawl links (e.g. 'friends' and 'interesting libraries')
# found on a user's LT profile.
FOLLOW_USER_CONNECTIONS = True