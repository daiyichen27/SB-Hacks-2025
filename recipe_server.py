from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from flask_cors import CORS

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app)  # Enable CORS for all routes

# Get API key from environment variable
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
if not SPOONACULAR_API_KEY:
    raise ValueError("SPOONACULAR_API_KEY environment variable is not set")

# Serve static files
@app.route('/')
def home():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/fridgecheck', methods=['GET', 'OPTIONS'])
def search_by_ingredients():
    # Handle preflight requests
    if request.method == 'OPTIONS':
        return '', 200
    
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
        print(response.json())
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
