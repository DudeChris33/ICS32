# LastFM.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

from WebAPI import WebAPI

# apikey = "9d1195a36107514345289454581c052a"
# secret = "3c28360dcc2043261ec91fe13d3fcd09"

"""
Response format:
<topartists country="Spain">
  <artist rank="1">
    <name>Coldplay</name>
    <playcount>3199</playcount>
    <mbid>cc197bad-dc9c-440d-a5b5-d52ba2e14234</mbid>
    <url>http://www.last.fm/music/Coldplay</url>
    <streamable>1</streamable>
    <image size="small">...</image>
    <image size="medium">...</image>
    <image size="large">...</image>
  </artist>
  ...
</topartists>
"""
"""
Errors:
2 : Invalid service - This service does not exist
3 : Invalid Method - No method with that name in this package
4 : Authentication Failed - You do not have permissions to access the service
5 : Invalid format - This service doesn't exist in that format
6 : Invalid parameters - Your request is missing a required parameter
7 : Invalid resource specified
8 : Operation failed - Something else went wrong
9 : Invalid session key - Please re-authenticate
10 : Invalid API key - You must be granted a valid key by last.fm
11 : Service Offline - This service is temporarily offline. Try again later.
13 : Invalid method signature supplied
16 : There was a temporary error processing your request. Please try again
26 : Suspended API key - Access for your account has been suspended, please contact Last.fm
29 : Rate limit exceeded - Your IP has made too many requests in a short period
"""

class LastFM(WebAPI):
    def __init__(self, country: str="spain"):
        try: country = str(country)
        except:
            print("Invalid country tag, defaulting to Spain")
            country = 'spain'
        if len(country.split()) != 1 or country in ("US", "USA", "UK", "GB"):
            print("Invalid country tag, defaulting to Spain")
            self.country = "spain"
        else:
            self.country = country
        
    
    def set_apikey(self, apikey:str="9d1195a36107514345289454581c052a") -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        :variable secret: LastFM provides a second key for authentication, but it is not used in this program
        '''
        if len(apikey.split()) != 1 or type(apikey) != str:
            self.apikey = "9d1195a36107514345289454581c052a"
        else:
            self.apikey = apikey
        self.secret = "3c28360dcc2043261ec91fe13d3fcd09"

    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        url = f"http://ws.audioscrobbler.com/2.0/?method=geo.gettopartists&country={self.country}&api_key={self.apikey}&format=json"
        r_obj = super()._download_url(url)
        self.r_obj = r_obj

        self.topartist_name = str(r_obj['topartists']['artist'][0]['name'])
        self.topartist_listeners = int(r_obj['topartists']['artist'][0]['listeners'])
        
    def transclude(self, message: str="@lastfm") -> str:
        try:
            message = str(message)
            new_message = f"{self.country.capitalize()}'s top artist is currently {self.topartist_name.title()} with {self.topartist_listeners:,} listeners"
            return message.replace('@lastfm', new_message)
        except:
            print("Invalid input")
        

if __name__ == "__main__":
    last_fm = LastFM()
    last_fm.set_apikey()
    last_fm.load_data()

    print(last_fm.transclude())