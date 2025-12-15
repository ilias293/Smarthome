import requests

def get_utc_temperature():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.09&longitude=5.12&current_weather=true"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        return data["current_weather"]["temperature"]
    except:
        return None
