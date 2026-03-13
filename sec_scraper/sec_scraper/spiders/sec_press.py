import scrapy

class SecPressSpider(scrapy.Spider):
    name = "sec_press"
    allowed_domains = ["sec.gov"]
    start_urls = ["https://www.sec.gov/newsroom/press-releases"]

    max_pages = 50
    page_count = 1

    custom_settings = {
        "DOWNLOAD_HANDLERS": {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
        "PLAYWRIGHT_BROWSER_TYPE": "chromium",
        "FEEDS": {"sec_press_releases.csv": {"format": "csv", "overwrite": True}},
        "DEFAULT_REQUEST_HEADERS": {
            "User-Agent": "MyUniversityDataResearchBot/1.0 (+hladdhad@purdue.edu)",
            "From": "hladdhad@purdue.edu",
            "Accept-Language": "en-US,en;q=0.9",
        },
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_MAX_DELAY": 5,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DOWNLOAD_DELAY": 1.0,
    }

    async def parse(self, response):
        self.logger.info(f"Parsing page {self.page_count}: {response.url}")

        # extract all press releases on current page
        for row in response.xpath("//tr[contains(@class,'pr-list-page-row')]"):
            yield {
                "Date": row.xpath(".//td[1]//time/text()").get(default="").strip(),
                "Headline": row.xpath(".//td[2]//a/text()").get(default="").strip(),
                "Link": response.urljoin(row.xpath(".//td[2]//a/@href").get("")),
                "Release No.": row.xpath(".//td[last()]/text()").get(default="").strip(),
            }

        # SEC pagination fix — detect using rel attribute or query param
        if self.page_count < self.max_pages:
            next_page = (
                response.xpath("//a[@rel='next']/@href").get()
                or response.xpath("//a[contains(@href, 'page=')]/@href").get()
            )

            if next_page:
                self.page_count += 1
                next_url = response.urljoin(next_page)
                self.logger.info(f"Following page {self.page_count}: {next_url}")
                yield scrapy.Request(
                    next_url,
                    meta={"playwright": True},
                    callback=self.parse,
                )
            else:
                self.logger.info("No further pagination link found — stopping.")
        else:
            self.logger.info(f"Reached max_pages={self.max_pages}, stopping crawl.")
