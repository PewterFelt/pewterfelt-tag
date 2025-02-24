from typing import TypedDict

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from flask import Flask, request
from langchain_community.llms.ollama import Ollama
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
{content}

---

Based on the previously given content give me a comma separated list of up to five most relevant tags you think best describe it.

---

Here's some examples:

If the content is about Neovim, you could tag it like `CLI,Tech,Lua,Neovim`.
If the content is a recipe, you could tag it like `Cooking,Recipe`.

---

Now return the list with no extra text, just the comma separated tags.
"""


# Define the expected request body structure
class TagRequest(TypedDict):
    url: str


app = Flask(__name__)


@app.route("/api/tag", methods=["POST"])
async def tag():
    # Get URL from request body
    data: TagRequest = request.get_json()
    if not data or "url" not in data:
        return {"error": "Missing URL in request body"}, 400  # pyright: ignore[reportUnreachable]

    url = data["url"]
    browser_config = BrowserConfig()
    run_config = CrawlerRunConfig()

    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            result = await crawler.arun(url=url, config=run_config)

            prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
            prompt = prompt_template.format(content=result)

            model = Ollama(model="llama3.2")
            response = model.invoke(prompt)

            return {"content": str(response)}

    except:
        return {"error": "error"}, 500
