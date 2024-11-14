import tensorflow as tf
import numpy as np

model=None

def load_model():
    global model
    model = tf.keras.models.load_model('model/mon_cnn_modele.h5') # relative path to /backend folder




def fit_data(image):
    """Fit inside of model and return predictions. Input is a 28x28 image like thoses in the MNIST project"""
    if model == None:
        load_model()

    try:
        prediction = model.predict(image)
        print(prediction)
        return {"err": None, "preds": np.reshape(prediction, -1).tolist()}
    except Exception as e:
        print(e)
        return {"err": "An error occured", "preds": None}
