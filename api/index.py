from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/<url>")
async def home(url: str):
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)

        return jsonify({"content": result})
