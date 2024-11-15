from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import numpy as np
import tensorflow as tf
from io import BytesIO

app = Flask(__name__)
cors = CORS(app)  # Allow CORS for all domains on all routes.
app.config['CORS_HEADERS'] = 'Content-Type'

# Global model variable to hold the loaded model
model = None

def load_model():
    global model
    if model is None:
        print("Loading model...")
        model = tf.keras.models.load_model('model/mon_cnn_modele.h5')
    return model

def clear_model_cache():
    global model
    print("Clearing model cache...")
    model = None

@app.route("/api/analyzeimage", methods=["POST"])
def analyze():
    """Route to receive image, process it, and get prediction."""
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    
    image_file = request.files['image']



    # FOR SAVING IMAGES AND IMPROVEING MODEL
    # filename = secure_filename(image_file.filename)
    # temp_path = os.path.join("model/uploads", filename)
    
    # if not os.path.exists('model/uploads'):
    #     os.makedirs('model/uploads')
    # image_file.save(temp_path)
    
    # Process image
    image_data = request.files['image'].read()
    image = Image.open(BytesIO(image_data))



    # the image sent by javascript contains the number pixels in the alpha chanel.
    # don't ask why. Just use this channel as the grayscale pixels
    image = np.array(image) 
    image = image[:, :, 3] 

    # Resize the image to 28x28 pixels --> MNIST image size, so what the model takes as input
    image = Image.fromarray(image).resize((28, 28))
    # Convert the image to a numpy array and normalize --> What MNIST DID
    image_array = np.array(image) / 255.0
    # Reshape the image to match the model's expected input shape (1, 28, 28, 1)
    image_array = image_array.reshape(1, 28, 28, 1)


    global model
    if model == None:
        model = load_model()

    try:
        prediction = model.predict(image_array)
        print("Prediction:", prediction)
        return {"preds": np.reshape(prediction, -1).tolist(), "err": None}
    except Exception as e:
        return {"err": str(e), "preds": None}

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
