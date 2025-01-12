import requests
import datetime
import time
import urllib.request
import json

class RateLimitedRequester:
    '''
    All HTTP requests throughout the program use this class. The variable
    self._last_call keeps track of the last call to the API to ensure the API's 
    terms of usage is followed. 
    '''
    def __init__(self, rate_limit_seconds = 1.0):
        self._last_call = None
        self._rate_limit_seconds = rate_limit_seconds

    def retrieve(self, params: dict):
        url = "https://api.spoonacular.com/recipes/findByIngredients"
        headers = {"x-api-key": "a52060d5687c4ccda3426ec492841a30"}

        current_time = datetime.datetime.now()
        if self._last_call:
            if (current_time - self._last_call).seconds < self._rate_limit_seconds:
                # print(f"Sleeping {self._rate_limit_seconds} seconds") # TODO: Remove print
                time.sleep(self._rate_limit_seconds)

        self._last_call = current_time

        formatted_params = ""
        if params:
            formatted_params = urllib.parse.urlencode(params)
        
        response = requests.get(url, headers=headers, params=formatted_params)

        # return response.json()
        return response.json()

if __name__ == '__main__':
    new_request = RateLimitedRequester()
    # ingredients = []
    # with open('input.txt', 'r') as file:
    #     for line in file:
    #         # Remove trailing newline and split on comma
    #         row = line.rstrip('\n').split(',') 
    #         for word in row:
    #             ingredients.extend(row)
    # print(ingredients)

    # https://inputdata

    input_url = "https://inputdata"
    user_input = requests.get(input_url)

    if user_input.status_code == 200:
        print(user_input.text)
    else:
        print(f"Error: {user_input.status_code}")

    params = {"ingredients": "cauliflower,onion,tomato", "number": "2"}

    try:
        data = new_request.retrieve(params)
        with open("data.json", "w") as file:
            json.dump(data, file)
    except IOError as e:
        print(f"An error occurred: {e}")
    
    print(new_request.retrieve(params))


# print(response.json())