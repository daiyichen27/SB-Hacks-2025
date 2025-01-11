import json
import urllib.request
import datetime
import time

class RateLimitedRequester:
    '''
    All HTTP requests throughout the program use this class. The variable
    self._last_call keeps track of the last call to the API to ensure the API's 
    terms of usage is followed. 
    '''
    def __init__(self, rate_limit_seconds = 1.0):
        self._last_call = None
        self._rate_limit_seconds = rate_limit_seconds

    def get(self, params: dict):
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        current_time = datetime.datetime.now()
        if self._last_call:
            if (current_time - self._last_call).seconds < self._rate_limit_seconds:
                # print(f"Sleeping {self._rate_limit_seconds} seconds") # TODO: Remove print
                time.sleep(self._rate_limit_seconds)

        self._last_call = current_time

        formatted_params = ""
        if params:
            formatted_params = urllib.parse.urlencode(params)
        formatted_url = url
        if formatted_params:
            formatted_url = f"{url}?{formatted_params}"
        # print(formatted_url)

        # APIKey: a52060d5687c4ccda3426ec492841a30
        headers = {"x-api-key": "a52060d5687c4ccda3426ec492841a30"}        
        request = urllib.request.Request(formatted_url, headers=headers)
        # request = urllib.request.Request(formatted_url)
        print(formatted_url)
        response = urllib.request.urlopen(request)

        response_data = response.read()
        # print(response_data)

        return json.loads(response_data)
    

if __name__ == '__main__':
    new_request = RateLimitedRequester()
    params = {"ingredients": "apples,flour,sugar", "number": "2"}
    print(new_request.get(params))
