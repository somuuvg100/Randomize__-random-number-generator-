from flask import Flask, render_template, request, jsonify
from typing import Tuple, Dict, Any
import random
import datetime

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def index() -> str:
    """Render the main index page."""
    return render_template("index.html")

@app.route("/api/generate", methods=["POST"])
def generate() -> Tuple[Any, int]:
    """
    Generate a random number within a specified range.
    
    Expects a JSON payload with 'minimum' and 'maximum' keys (can be strings or ints).
    Returns a JSON object with the generated value, the range used, and an ISO timestamp.
    """
    # Get JSON payload, defaulting to an empty dict if invalid or missing
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    
    try:
        minimum = int(data.get("minimum", ""))
        maximum = int(data.get("maximum", ""))
    except (ValueError, TypeError):
        return jsonify({"error": "Please provide valid integers for minimum and maximum."}), 400
        
    if minimum > maximum:
        return jsonify({"error": "Minimum cannot be greater than maximum."}), 400
        
    # Generate the random value and current timestamp
    value = random.randint(minimum, maximum)
    timestamp = datetime.datetime.now().isoformat()
    
    return jsonify({
        "value": value, 
        "range": [minimum, maximum], 
        "timestamp": timestamp
    }), 200

if __name__ == "__main__":
    # Run the application in debug mode for development
    app.run(debug=True, port=5000)