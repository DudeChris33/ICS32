# test.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

from WebAPI import WebAPI
from OpenWeather import OpenWeather
from LastFM import LastFM

def test_api(message:str, apikey:str, webapi:WebAPI):
    webapi.set_apikey(apikey)
    webapi.load_data()
    result = webapi.transclude(message)
    print(result)


open_weather = OpenWeather() #notice there are no params here...HINT: be sure to use parameter defaults!!!
lastfm = LastFM()

test_api("Testing the weather: @weather", "b186c8cbfb7b0e1bcf52b5d52da652eb", open_weather)
# expected output should include the original message transcluded with the default weather value for the @weather keyword.

test_api("Testing lastFM: @lastfm", "9d1195a36107514345289454581c052a", lastfm)
# expected output include the original message transcluded with the default music data assigned to the @lastfm keyword