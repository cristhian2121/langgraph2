from langchain_core.tools import tool
import requests

@tool("get_city_cordinates")
def get_city_cordinates(city: str):
    """Return coordinates by city"""
    from urllib.parse import quote

    url = f"https://geocoding-api.open-meteo.com/v1/search?name={quote(city)}&count=1&language=es&format=json"
    response = requests.get(url)
    data = response.json()

    if "results" not in data or not data["results"]:
        return []

    result = data["results"][0]
    latitude = result["latitude"]
    longitude = result["longitude"]

    return [latitude, longitude]

@tool("check_weather")
def check_weather(latitude="-40.157", longitude="-71.353"):
    "Get weather for a specified location"
    print("[latitude]", latitude)
    print("[longitude]", longitude)
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current_weather=true")
    weather = response.json()

    return weather