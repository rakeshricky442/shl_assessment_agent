import json
from pathlib import Path


CATALOG_PATH = Path("data/catalog.json")


def load_catalog():
    """
    Load the SHL product catalog from JSON.
    """

    with open(CATALOG_PATH, "r", encoding="utf-8") as file:
        catalog = json.load(file)

    return catalog


def main():

    catalog = load_catalog()

    print("=" * 50)
    print("SHL Catalog Loaded Successfully")
    print("=" * 50)

    print(f"\nTotal Assessments : {len(catalog)}")

    print("\nFirst Assessment\n")

    print(json.dumps(catalog[0], indent=4))


if __name__ == "__main__":
    main()