import csv
import json
import os
import requests

url = "https://api.github.com/search/repositories"
params = {
    "q": "machine learning",
    "sort": "stars",
    "order": "desc",
    "per_page": 10
}
json_file = "ai_repositories.json"
csv_file = "ai_repositories.csv"

try:
    response = requests.get(url, params=params, timeout=10)
    print("HTTP status:", response.status_code)
    response.raise_for_status()
    data = response.json()

    items = data.get("items")
    if not isinstance(items, list):
        raise ValueError("API response does not contain a repository list.")

    records = []
    for item in items:
        records.append({
            "name": item.get("full_name", ""),
            "stars": int(item.get("stargazers_count", 0)),
            "language": item.get("language") or "Unknown",
            "url": item.get("html_url", "")
        })

    if records:
        average_stars = sum(item["stars"] for item in records) / len(records)
        highest = max(records, key=lambda item: item["stars"])
        language_counts = {}
        for item in records:
            language_counts[item["language"]] = language_counts.get(item["language"], 0) + 1

        print("Average stars:", average_stars)
        print("Most-starred repository:", highest)
        print("Language counts:", language_counts)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4)

    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        fields = ["name", "stars", "language", "url"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

except requests.exceptions.Timeout:
    print("API request timed out.")
except requests.exceptions.ConnectionError:
    print("Could not connect to GitHub API.")
except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)
except requests.exceptions.RequestException as error:
    print("API request failed:", error)
except (ValueError, TypeError, KeyError) as error:
    print("Invalid JSON or missing data:", error)
except FileNotFoundError as error:
    print("File not found:", error)
except OSError as error:
    print("File error:", error)
else:
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            saved_json = json.load(file)
        with open(csv_file, "r", newline="", encoding="utf-8") as file:
            saved_csv = list(csv.DictReader(file))

        print("JSON records verified:", len(saved_json))
        print("CSV records verified:", len(saved_csv))
    except FileNotFoundError as error:
        print("Saved file not found:", error)
    except json.JSONDecodeError as error:
        print("Saved JSON is invalid:", error)
    except OSError as error:
        print("Could not read saved files:", error)
finally:
    print("Pipeline finished.")
