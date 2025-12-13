import os
import requests

class fetch_weather:
    def __init__(self):
        self.city="Pune"
        self.weather_url=os.getenv("WEATHER_URL")
        self.lat_long_url=os.getenv("LAT_LONG_URL")
        self.weather_api=os.getenv("WEATHER_API_KEY")

    def lat_long_data(self, city):
        lat_params={"q":self.city, "appid":self.weather_api}
        lat_long_data=requests.get(self.lat_long_url, lat_params)
        return lat_long_data.json()
    
    def fetch_weather_data(self, city):
        coords_data=self.lat_long_data(self.city)
        lat=coords_data[0]["lat"]
        long=coords_data[0]["lon"]
        weather_params={"lat":lat, "lon":long, "appid":self.weather_api}
        weather_data=requests.get(self.weather_url, weather_params)
        return weather_data.json()
    
    def extract_data(self, data):
        weather_details={
            "description": data["weather"][0]["description"],
            "temp": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
        }

        if "rain" in data:
            weather_details["rain"]=data["rain"]["1h"]

        return weather_details
    
    def get_weather(self):
        data=self.fetch_weather_data(self.city)
        return self.extract_data(data)