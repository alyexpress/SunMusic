from config import WEATHER_URL
import requests


class Weather:
    def __init__(self, api_key):
        self.url = WEATHER_URL
        self.api_key = api_key

    def get(self, city):
        params = {'q': city, 'units': 'metric',
                  'lang': 'ru', 'APPID': self.api_key}
        response = requests.get(self.url, params=params)
        data = response.json()
        if data['cod'] == "404":
            return None
        temp = data['main']['temp']
        weather = data['weather'][0]['main']
        description = data['weather'][0]['description']
        wind = data['wind']['speed']
        clouds = data['clouds']['all']
        return temp, weather, description, wind, clouds
