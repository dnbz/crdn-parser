from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import os

load_dotenv()

# Scrapy settings for kolesa_parser project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html


SPIDER_MODULES = ["kolesa_parser.spiders"]
NEWSPIDER_MODULE = "kolesa_parser.spiders"

BASEURL = "https://kolesa.kz"
DOMAIN_NAME = "kolesa.kz"

CONNECTION_STRING = os.environ.get(
    "DB_CONNECTION", "postgresql://user:password@127.0.0.1:5432/parser"
)

PARSER_NODE = os.environ.get("PARSER_NODE", "node-2")

KOLESA_MAX_PAGES = int(os.environ.get("MAX_PAGES", 1000))

KOLESA_IMG_SIZE = "750x470"

EXCHANGE_KEYWORDS = ["обмен", "меняю", "ключ на ключ"]
NO_EXCHANGE_KEYWORDS = [
    "не меняю",
    "без обмен",
    "нет обмен",
    "обмена нет",
    "обмен жок",
    "обмен жоқ"
    "обмена жоқ"
    "обмена жок",
    "обмен не предлагать",
    "обмены не предлагать",
    "обмен не интересует",
    "обмены не интересуют",
]

# сколько страниц без новых объявлений нужно пройти, перед тем как остановиться
PAGE_STOP_NO_NEW = os.environ.get("PARSER_PAGE_STOP_NO_NEW")
# количество объявлений на странице
PAGE_SIZE = 20

STDOUT_LOG = bool(os.environ.get("STDOUT_LOG", False))

if not STDOUT_LOG:
    LOG_FILE = Path.cwd() / ("logs/" + datetime.now().strftime("%Y-%m-%d") + "_parser.log")

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
CONCURRENT_REQUESTS_PER_DOMAIN = 1

MOBILE_REDIRECT_DELAY = 2

DOWNLOAD_TIMEOUT = 3

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Disable cookies (enabled by default)
COOKIES_ENABLED = True


# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = True

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'kolesa_parser.middlewares.KolesaParserSpiderMiddleware': 543,
# }
#
#

ROTATING_PROXY_PAGE_RETRY_TIMES = 10

# dealing with redirects to mobile version
RETRY_HTTP_CODES = [302]

DISABLE_PROXY = os.environ.get("DISABLE_PROXY")

if not DISABLE_PROXY:
    ROTATING_PROXY_LIST_PATH = Path.cwd() / "proxies.txt"

FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",  # this is the first provider we'll try
    "scrapy_fake_useragent.providers.FakerProvider",  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",  # fall back to USER_AGENT value
]

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # 'kolesa_parser.middlewares.KolesaParserDownloaderMiddleware': 543,
    "rotating_proxies.middlewares.RotatingProxyMiddleware": 591,
    "rotating_proxies.middlewares.BanDetectionMiddleware": 592,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 593,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 594,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "kolesa_parser.pipelines.SaveCarPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
