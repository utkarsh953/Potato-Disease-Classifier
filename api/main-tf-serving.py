from fastapi import FastAPI,File, UploadFile
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf
from tensorflow import keras
import requests
# This file is created for changes related to Tf serving related changes.
# can be ignored if tf serving is not being, main.py is fine then.
app = FastAPI()

endpoint= "http://localhost:8506/v1/models/potatoes_model:predict"

MODEL = tf.keras.models.load_model('../saved_models/model_1.keras')
CLASS_NAMES = ["Early Blight","Late Blight","Healthy"]

def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image

@app.get("/ping")
async def ping():
    return "Hello I am alive."

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image,0)
    json_data = {
        "instances": img_batch.tolist()
    }
    response = requests.post(endpoint,json=json_data)
    prediction = np.array(response.json()["predictions"][0])
    predicted_class = CLASS_NAMES[np.argmax(prediction)]
    confidence = np.max(confidence)
    return {
        'class': predicted_class,
        'confidence': float(confidence)
    }


if __name__ =="__main__":   
    uvicorn.run(app,host='localhost',port=8000) 