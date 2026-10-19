import os
import html
import requests

AUTHOR_ID = "9PY80DQAAAAJ"
API_KEY = os.environ["SERPAPI_KEY"]

url = "https://serpapi.com/search"

params = {
    "engine": "google_scholar_author",
    "author_id": AUTHOR_ID,
    "hl": "en",
    "api_key": API_KEY,
}

response = requests.get(url, params=params, timeout=30)
response.raise_for_status()
data = response.json()

if "error" in data:
    raise RuntimeError(data["error"])

table = data["cited_by"]["table"]

citations = None
h_index = None

for item in table:
    if "citations" in item:
        citations = item["citations"]["all"]
    elif "h_index" in item:
        h_index = item["h_index"]["all"]

if citations is None or h_index is None:
    raise RuntimeError(f"Could not parse citation metrics: {table}")

citations_text = f"{citations:,}"
h_text = str(h_index)

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="325" height="28"
     viewBox="0 0 325 28"
     role="img"
     aria-label="Google Scholar: {html.escape(citations_text)} citations, h-index {html.escape(h_text)}">
  <text x="0" y="19"
        font-family="Arial, Helvetica, sans-serif"
        font-size="13"
        fill="#555555">
    <tspan font-weight="600">Google Scholar</tspan>
    <tspan> · {html.escape(citations_text)} citations · h-index {html.escape(h_text)}</tspan>
  </text>
</svg>
"""

with open("scholar-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(
    f"Updated scholar-stats.svg: "
    f"{citations_text} citations, h-index {h_text}"
)
