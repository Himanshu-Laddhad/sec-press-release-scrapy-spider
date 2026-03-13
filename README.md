# HW6 – SEC Press Release Scraper (Scrapy + Playwright)

**Course:** MGTA 590 – Web Data Analytics | Purdue University
**Skills:** Python · Scrapy · Playwright · Async Scraping · XPath · Pagination · Responsible Crawling

---

## Overview

This project is a production-grade web crawler built with **Scrapy** and **scrapy-playwright** that scrapes press releases from the [SEC.gov Newsroom](https://www.sec.gov/newsroom/press-releases). Because SEC's press release listing page uses JavaScript for rendering and pagination, a headless Chromium browser (via Playwright) is integrated directly into the Scrapy pipeline to fully render each page before extraction.

The spider crawls up to 50 pages, extracting the date, headline, article link, and release number for each press release, and exports the results to a CSV file.

---

## What It Does

1. **Launches headless Chromium** via Playwright for JavaScript rendering
2. **Extracts from each listing page:**
   - Publication date
   - Headline text
   - Full article URL
   - Release number (e.g., `2025-129`)
3. **Follows pagination** automatically using `rel="next"` or `?page=` link detection
4. **Respects rate limits** via AutoThrottle (1–5s adaptive delay, max 2 concurrent requests)
5. **Identifies the crawler** with a university research User-Agent and contact email
6. **Exports** all results to `sec_press_releases.csv`

---

## Project Structure

```
sec_scraper/
├── scrapy.cfg
└── sec_scraper/
    ├── __init__.py
    ├── items.py          # Item schema definition
    ├── middlewares.py
    ├── pipelines.py
    ├── settings.py
    └── spiders/
        └── sec_press.py  # Main spider
sec_press_releases.csv    # Output data
```

---

## Output Schema

```
Date, Headline, Link, Release No.
"Sept. 30, 2025", "SEC Announces...", https://www.sec.gov/..., 2025-129
```

---

## Sample Data

| Date | Headline | Release No. |
|---|---|---|
| Sept. 30, 2025 | SEC Announces Departure of Director... | 2025-129 |
| Sept. 30, 2025 | SEC Continues Efforts to Assist Market Participants... | 2025-128 |

---

## Key Concepts Demonstrated

| Concept | Description |
|---|---|
| Scrapy spider architecture | `start_urls`, `parse()`, `yield` items & requests |
| Playwright integration | Headless browser for JS-rendered pages |
| XPath selectors | Precise extraction from table rows |
| Async pagination | `rel="next"` detection with fallback `?page=` |
| AutoThrottle | Adaptive rate limiting to avoid server overload |
| Responsible crawling | Custom `User-Agent` with contact info, `DOWNLOAD_DELAY` |
| CSV feed export | `FEEDS` setting for automatic CSV output |

---

## Tech Stack

- **Language:** Python 3
- **Framework:** Scrapy
- **Browser Automation:** scrapy-playwright (Chromium)
- **Output:** CSV via Scrapy FEEDS

---

## Prerequisites

```bash
pip install scrapy scrapy-playwright
playwright install chromium
```

---

## How to Run

```bash
cd sec_scraper
scrapy crawl sec_press
```

Output will be written to `sec_press_releases.csv` in the project root (overwriting any existing file).

To limit the number of pages crawled, edit `max_pages` in `sec_press.py`:

```python
max_pages = 10  # Scrape only the first 10 pages
```

---

## Responsible Scraping

This spider implements several best practices for ethical crawling:

- **Identifies itself** with a descriptive `User-Agent` and institutional email
- **AutoThrottle** dynamically adjusts delays based on server response times
- **Limits concurrency** to 2 requests per domain
- **Fixed download delay** of 1 second between requests
- SEC.gov is a U.S. government public data source — data is freely available for research
