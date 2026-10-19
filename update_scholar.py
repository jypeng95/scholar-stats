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
i10_index = None

for item in table:
    if "citations" in item:
        citations = item["citations"]["all"]
    elif "h_index" in item:
        h_index = item["h_index"]["all"]
    elif "i10_index" in item:
        i10_index = item["i10_index"]["all"]

if citations is None or h_index is None:
    raise RuntimeError(f"Could not parse citation metrics: {table}")

citations_text = f"{citations:,}"
h_text = str(h_index)
i10_text = str(i10_index) if i10_index is not None else "—"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
     width="500" height="64"
     viewBox="0 0 500 64"
     role="img"
     aria-label="Google Scholar metrics">
  <rect width="500" height="64" rx="8" fill="#f7f7f7"/>
  <text x="18" y="26"
        font-family="Arial, Helvetica, sans-serif"
        font-size="15"
        font-weight="600"
        fill="#333333">
    Google Scholar
  </text>
  <text x="18" y="48"
        font-family="Arial, Helvetica, sans-serif"
        font-size="14"
        fill="#555555">
    {html.escape(citations_text)} citations · h-index {html.escape(h_text)} · i10-index {html.escape(i10_text)}
  </text>
</svg>
"""

with open("scholar-stats.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print(
    f"Updated scholar-stats.svg: "
    f"{citations_text} citations, h-index {h_text}, i10-index {i10_text}"
)
