import json
from pathlib import Path


class CatalogService:
    """
    Service class for loading and querying the SHL product catalog.
    """

    def __init__(self):
        self.catalog_path = Path("data/catalog.json")
        self.catalog = self.load_catalog()

    def load_catalog(self):
        """
        Load catalog.json from the data folder.
        """
        with open(self.catalog_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def get_all(self):
        """
        Return all assessments.
        """
        return self.catalog

    def search_by_name(self, keyword):
        """
        Search assessments by name.
        """
        keyword = keyword.lower().strip()

        results = []

        for assessment in self.catalog:
            name = assessment.get("name", "").lower()

            if keyword in name:
                results.append(assessment)

        return results


def main():
    service = CatalogService()

    print("=" * 60)
    print("SHL CATALOG SERVICE")
    print("=" * 60)

    print(f"Total Assessments : {len(service.get_all())}")

    keyword = input("\nEnter assessment name to search: ")

    results = service.search_by_name(keyword)

    print("\n" + "=" * 60)
    print(f"Found {len(results)} matching assessment(s)")
    print("=" * 60)

    if not results:
        print("No assessments found.")
        return

    for i, assessment in enumerate(results, start=1):
        print(f"\nAssessment {i}")
        print("-" * 40)
        print(f"Name       : {assessment.get('name', 'N/A')}")
        print(f"Duration   : {assessment.get('duration', 'N/A')}")
        print(f"Remote     : {assessment.get('remote', 'N/A')}")
        print(f"Adaptive   : {assessment.get('adaptive', 'N/A')}")
        print(f"URL        : {assessment.get('link', 'N/A')}")
        print(f"Description: {assessment.get('description', 'N/A')}")


if __name__ == "__main__":
    main()