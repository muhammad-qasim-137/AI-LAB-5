import requests

base_url = "https://jsonplaceholder.typicode.com/posts"
sample = {
    "title": "Image classification",
    "body": "Example computer vision prediction input",
    "userId": 1
}


def show_response(label, response):
    print("\\n" + label)
    print("HTTP status:", response.status_code)
    try:
        print("JSON response:", json_text(response))
    except ValueError:
        print("Response was not valid JSON.")


def json_text(response):
    import json
    return json.dumps(response.json(), indent=4)


try:
    response = requests.get(base_url + "/1", timeout=10)
    show_response("GET", response)
    response.raise_for_status()

    response = requests.post(base_url, json=sample, timeout=10)
    show_response("POST", response)
    response.raise_for_status()

    response = requests.put(base_url + "/1", json=sample, timeout=10)
    show_response("PUT", response)
    response.raise_for_status()

    response = requests.patch(base_url + "/1", json={"title": "Updated image prediction"}, timeout=10)
    show_response("PATCH", response)
    response.raise_for_status()

    response = requests.delete(base_url + "/1", timeout=10)
    print("\\nDELETE")
    print("HTTP status:", response.status_code)
    print("Response body:", response.text or "(empty response)")
    response.raise_for_status()

    print("\\nOperations completed. JSONPlaceholder simulates writes; it does not permanently change server data.")

except requests.exceptions.Timeout:
    print("The request timed out.")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API.")
except requests.exceptions.HTTPError as error:
    print("HTTP error:", error)
except requests.exceptions.RequestException as error:
    print("API request failed:", error)
except ValueError as error:
    print("Invalid JSON response:", error)
