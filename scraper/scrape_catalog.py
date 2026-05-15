import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://www.shl.com"

CATALOG_URL = (
    "https://www.shl.com/solutions/products/product-catalog/"
)

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(
    CATALOG_URL,
    headers=headers
)

soup = BeautifulSoup(
    response.text,
    "html.parser"
)

links = soup.find_all("a")

product_links = []

for link in links:

    href = link.get("href")

    if href and "/products/" in href:

        if href.startswith("/"):

            href = BASE_URL + href

        product_links.append(href)

product_links = list(set(product_links))

catalog = []

for url in product_links:

    try:

        print(f"Scraping: {url}")

        res = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        page = BeautifulSoup(
            res.text,
            "html.parser"
        )

        title = ""

        if page.title:
            title = page.title.text.strip()

        description = ""

        meta_desc = page.find(
            "meta",
            attrs={"name": "description"}
        )

        if meta_desc:

            description = meta_desc.get(
                "content",
                ""
            )

        page_text = page.get_text(
            separator=" ",
            strip=True
        )

        item = {
            "name": title,
            "url": url,
            "description": description,
            "content": page_text[:5000]
        }

        catalog.append(item)

        time.sleep(1)

    except Exception as e:

        print(f"Error: {e}")

with open("app/catalog.json", "w", encoding="utf-8") as f:

    json.dump(
        catalog,
        f,
        indent=2,
        ensure_ascii=False
    )

print(f"Saved {len(catalog)} assessments")