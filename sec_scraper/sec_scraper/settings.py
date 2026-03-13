# Scrapy settings for sec_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "sec_scraper"

SPIDER_MODULES = ["sec_scraper.spiders"]
NEWSPIDER_MODULE = "sec_scraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": "MyUniversityDataResearchBot/1.0 (hladdhad@purdue.edu)",
    "From": "hladdhad@purdue.edu",
}


# Obey robots.txt rules
ROBOTSTXT_OBEY = True
# Concurrency and throttling settings
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 2
DOWNLOAD_DELAY = 2


# Optional: handle retries and timeouts gracefully
RETRY_ENABLED = True
RETRY_TIMES = 3
DOWNLOAD_TIMEOUT = 15

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "sec_scraper.pipelines.SecScraperPipeline": 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
DOWNLOAD_DELAY = 1.0  # be polite
AUTOTHROTTLE_START_DELAY = 1.0
AUTOTHROTTLE_MAX_DELAY = 5.0
CONCURRENT_REQUESTS_PER_DOMAIN = 2

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

FEEDS = {
    "sec_press_releases.csv": {"format": "csv", "overwrite": True},
}

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# Use Playwright for JS rendering
# Playwright integration
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"


PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,   # Run without opening browser window
    "timeout": 30000
}



