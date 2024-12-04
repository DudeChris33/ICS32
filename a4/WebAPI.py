# WebAPI.py

# Chris Cyr
# cyrc@uci.edu
# 12436037

import json
from urllib import request, error
from abc import ABC, abstractmethod

class WebAPI(ABC):
    @classmethod
    def _download_url(self, url: str) -> dict:
        response = None
        r_obj = None

        try:
            response = request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)
        except error.HTTPError as ex:
            print('Failed to download contents of URL')
            print(f'Status code: {ex.code}')
        except json.JSONDecodeError:
            print('Failed to decode message from api')
        except error.URLError:
            print('Internet connection lost')
        else:
            pass
            # print('An unknown error has occurred')
        finally:
            if response != None: response.close()

        return r_obj
    
    @abstractmethod
    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service   
        '''
        pass

    @abstractmethod
    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
        '''
        pass

    @abstractmethod
    def transclude(self, message: str) -> str:
        pass