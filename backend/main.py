from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from PIL import Image
import numpy as np

from model.prod_model import fit_data

app = Flask(__name__)
cors = CORS(app) # allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/api/analyzeimage", methods=["POST"])
def analyze():
    """Route supposed to get image from body (28x28) and feed it to model to analyze and return results. 
    Also need to save it in a folder waiting for user to tell us if the model was right"""


    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']
    
    # Making sure the image is the good size...
    image = Image.open(image_file).convert('L')
    image = image.resize((28, 28))
    image_array = np.array(image) / 255.0  
    image_array = image_array.reshape(1, 28, 28, 1)
    results = fit_data(image_array)

    return results

@app.route("/api/confirmprediction", methods=["POST"])
def confirm():
    return "thanks"

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)