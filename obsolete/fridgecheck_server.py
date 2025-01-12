from flask import Flask, request, jsonify
import requests
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("SPOONACULAR_API_KEY environment variable is not set")

@app.route('/fridgecheck', methods=['GET'])
def search_by_ingredients():
    # Get ingredients from query parameter
    ingredients = request.args.get('ingredients')
    if not ingredients:
        return jsonify({"error": "No ingredients provided"}), 400

    # Spoonacular API endpoint
    url = "https://api.spoonacular.com/recipes/findByIngredients"
    
    # Headers for the API request
    headers = {
        'x-api-key': SPOONACULAR_API_KEY
    }
    
    # Parameters for the API request
    params = {
        'ingredients': ingredients,
        'number': 10,  # Number of results to return
        'ranking': 2,  # Maximize used ingredients
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for error status codes
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
