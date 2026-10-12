import requests

# Open-Meteo is a public forecast API. Forecast temperature is the predicted result;
# this API does not provide a confidence score, so the program reports that honestly.
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 24.8607,
    "longitude": 67.0011,
    "daily": "temperature_2m_max",
    "forecast_days": 1,
    "timezone": "Asia/Karachi"
}

try:
    response = requests.get(url, params=params, timeout=10)
    print("HTTP status:", response.status_code)
    response.raise_for_status()
    data = response.json()

    dates = data.get("daily", {}).get("time", [])
    predictions = data.get("daily", {}).get("temperature_2m_max", [])
    if not dates or not predictions:
        raise ValueError("The response did not contain forecast data.")

    print("Input location: Karachi, Pakistan")
    print("Prediction date:", dates[0])
    print("Predicted maximum temperature:", predictions[0], "°C")
    print("Confidence score: Not supplied by this API.")

except requests.exceptions.Timeout:
    print("Request timed out. Try again later.")
except requests.exceptions.ConnectionError:
    print("Could not connect to the prediction service.")
except requests.exceptions.HTTPError as error:
    print("The API returned an HTTP error:", error)
except requests.exceptions.RequestException as error:
    print("Request failed:", error)
except (ValueError, KeyError, TypeError) as error:
    print("Invalid or incomplete API response:", error)
