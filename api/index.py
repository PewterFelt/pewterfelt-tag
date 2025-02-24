from typing import TypedDict

from flask import Flask, request
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI

PROMPT_TEMPLATE = """
{content}

* * *

Analyze the content and generate up to five relevant tags that best represent its core topics. Follow these guidelines:

1. Prioritize specific terms over general ones
2. Use lower case with spaces (e.g., "machine learning")
3. Use uppercase without dots for acronyms (e.g., "UI", "CLI", "AI", "ETF")
4. Have no spaces around the commas, only for compound meanings (e.g., "machine learning", "web development", "climate change")
4. Maximum 5 tags, minimum 2

* * *

Examples:
- Neovim configuration guide → `CLI,tech,lua,neovim,IDE`
- Python web development tutorial → `python,web development,backend,programming,tech`
- Healthy meal recipe → `cooking,recipe,nutrition,healthy eating`
- React performance optimization → `web development,react,javascript`
- Climate change analysis → `environment,science,climate change,sustainability`
- Personal finance tips → `finance,personal finance,money management,investing`
- Machine learning fundamentals → `AI,machine learning,data science,mathematics`
- Travel guide to Japan → `travel,japan,culture,tourism`

* * *

Return only a comma-separated list of tags with no additional formatting or explanation.
"""


class TagRequest(TypedDict):
    content: str


def tag_content(content: str):
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(content=content)

    model = GoogleGenerativeAI(model="gemini-2.0-flash-exp")

    return model.invoke(prompt)


app = Flask(__name__)


@app.route("/api/tag", methods=["POST"])
async def tag():
    data: TagRequest = request.get_json()
    if not data or "content" not in data:
        return {"error": "Missing content in request body"}, 400  # pyright: ignore[reportUnreachable]

    content = data["content"]

    try:
        tags = tag_content(content)
    except Exception:
        return {"error": "Failed to tag content"}, 500

    return {"tags": str(tags)}
