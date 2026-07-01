import requests

BASE_URL = "https://www.shl.com/solutions/products/product-catalog/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/137.0.0.0 Safari/537.36"
    )
}


def fetch_catalog_page():
    """
    Download the SHL Product Catalog page.
    """

    response = requests.get(
        BASE_URL,
        headers=HEADERS,
        timeout=30
    )

    response.raise_for_status()

    return response.text


def save_html(html):
    """
    Save downloaded HTML locally.
    """

    with open("data/catalog_page.html", "w", encoding="utf-8") as file:
        file.write(html)


def main():

    print("=" * 50)
    print("Downloading SHL Product Catalog...")
    print("=" * 50)

    html = fetch_catalog_page()

    print(f"Downloaded {len(html)} characters.")

    save_html(html)

    print("HTML saved successfully!")
    print("Location: data/catalog_page.html")


if __name__ == "__main__":
    main()