import csv
import json
import requests

query = input("Enter a text search query: ").strip() or "machine learning"
url = "https://hn.algolia.com/api/v1/search"
params = {"query": query, "hitsPerPage": 10}

try:
    response = requests.get(url, params=params, timeout=10)
    print("HTTP status:", response.status_code)
    response.raise_for_status()
    data = response.json()
    hits = data.get("hits")
    if not isinstance(hits, list):
        raise ValueError("Unexpected response format.")

    records = []
    for hit in hits:
        text = hit.get("story_text") or hit.get("comment_text") or hit.get("title") or ""
        if text.strip():
            records.append({
                "text": text,
                "author": hit.get("author", ""),
                "source": hit.get("url") or hit.get("story_url") or "",
                "created_at": hit.get("created_at", ""),
                "object_id": hit.get("objectID", "")
            })

    print("Retrieved text records:", len(records))
    for record in records:
        print("\\nText:", record["text"])
        print("Author:", record["author"])
        print("Source:", record["source"])
        print("Created at:", record["created_at"])

    with open("nlp_text_data.json", "w", encoding="utf-8") as file:
        json.dump(records, file, indent=4, ensure_ascii=False)

    with open("nlp_text_data.csv", "w", newline="", encoding="utf-8") as file:
        fields = ["text", "author", "source", "created_at", "object_id"]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(records)

    print("Saved to nlp_text_data.json and nlp_text_data.csv.")

except requests.exceptions.Timeout:
    print("The request timed out.")
except requests.exceptions.ConnectionError:
    print("Could not connect to the text API.")
except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)
except requests.exceptions.RequestException as error:
    print("Request failed:", error)
except (ValueError, TypeError) as error:
    print("Invalid API response:", error)
except OSError as error:
    print("File error:", error)
