import requests

def get_utc_temperature():
    """
    Haal de actuele temperatuur in Utrecht op via Open-Meteo API.
    Retourneert de temperatuur in °C of None als er een probleem is.
    """
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=52.0907&longitude=5.1214&current_weather=true"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data["current_weather"]["temperature"]
    except:
        return None
