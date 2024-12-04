# OpenWeather.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

from WebAPI import WebAPI
from datetime import datetime

"""
Response format:
{
    "coord": {"lon": float, "lat": float},
    "weather": [{"id": int, "main": str, "description": str, "icon": str}],
    "base": str,
    "main": {"temp": float, "feels_like": float, "temp_min": float, "temp_max": float, "pressure": int, "humidity": int},
    "visibility": int,
    "wind": {"speed": float, "deg": float},
    "clouds": {"all": int},
    "dt": int,
    "sys": {"type": int, "id": int, "message": float, "country": str, "sunrise": int, "sunset": int},
    "timezone": int,
    "id": int,
    "name": str,
    "cod": int
}
"""

class OpenWeather(WebAPI):
    def __init__(self, zip: int=92697, ccode: str="US"):
        try: self.zip = int(zip)
        except: print("Invalid zip code, defaulting to Irvine")
        try: self.ccode = str(ccode)
        except: print("Invalid country code, defaulting to United States")
    
    def set_apikey(self, apikey:str="security") -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        '''
        if len(apikey.split()) != 1 or type(apikey) != str:
            print("Invalid apikey, defaulting to mine")
            with open("OpenWeatherApiKey.txt", "r") as f:
                contents = f.readlines()
                self.apikey = str(contents[0].rstrip().split("=")[1])
        else:
            self.apikey = apikey

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        url = f"http://api.openweathermap.org/data/2.5/weather?zip={self.zip},{self.ccode}&appid={self.apikey}&units=imperial"
        r_obj = super()._download_url(url)
        self.r_obj = r_obj
        
        self.longitude = r_obj['coord']['lon']
        self.latitude = r_obj['coord']['lat']

        source = r_obj['weather'][0]
        # self.weather_id = source['id']
        # self.weather_main = source['main']
        self.description = source['description']
        # self.weather_icon = source['icon']

        source = r_obj['main']
        self.temperature = source['temp']
        self.feels_like = source['feels_like']
        self.low_temperature = source['temp_min']
        self.high_temperature = source['temp_max']
        self.pressure = source['pressure']
        self.humidity = str(source['humidity']) + '%' + ' cloud coverage'

        self.visibility = r_obj['visibility']

        # self.wind_speed = r_obj['wind']['speed']
        # self.wind_direction = r_obj['wind']['deg']

        self.clouds = str(r_obj['clouds']['all']) + "%"
        self.timestamp = r_obj['dt']

        source = r_obj['sys']
        self.country = source['country']
        self.sunrise = datetime.utcfromtimestamp(source['sunrise'])
        self.sunset = datetime.utcfromtimestamp(source['sunset'])

        self.timezone = r_obj['timezone']
        self.city_id = r_obj['id']
        self.city = r_obj['name']

    def transclude(self, message: str='@weather') -> str:
        try:
            message = str(message)
            return message.replace('@weather', str(self.clouds))
        except:
            print("Invalid input")
        

# if __name__ == "__main__":
#     open_weather = OpenWeather()
#     open_weather.set_apikey()
#     open_weather.load_data()

#     print(f"The temperature for {92697} is {open_weather.temperature} degrees")
#     print(f"The high for today in {92697} will be {open_weather.high_temperature} degrees")
#     print(f"The low for today in {92697} will be {open_weather.low_temperature} degrees")
#     print(f"The coordinates for {92697} are {open_weather.longitude} longitude and {open_weather.latitude} latitude")
#     print(f"The current weather for {92697} is {open_weather.description}")
#     print(f"The current humidity for {92697} is {open_weather.humidity}")
#     print(f"The sun will set in {open_weather.city} at {open_weather.sunset}")