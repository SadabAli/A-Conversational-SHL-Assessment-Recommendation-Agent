import requests
from bs4 import BeautifulSoup
import json

CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(CATALOG_URL, headers=headers)

print(response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a")

catalog = []

for link in links:

    href = link.get("href")

    text = link.get_text(strip=True)

    if href and "/products/" in href:

        item = {
            "name": text,
            "url": href
        }

        catalog.append(item)

unique_catalog = []

seen = set()

for item in catalog:

    if item["url"] not in seen:

        seen.add(item["url"])

        unique_catalog.append(item)

with open("app/catalog.json", "w") as f:

    json.dump(unique_catalog, f, indent=2)

print(f"Saved {len(unique_catalog)} items")