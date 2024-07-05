from fastapi import FastAPI, File, UploadFile, HTTPException, Annotated
from keras.models import load_model
from tensorflow.keras.utils import img_to_array
from PIL import Image
import numpy as np
import uvicorn
import uuid
import os

app = FastAPI()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(CURRENT_DIR, "./models/braintumor.h5")
LABELS_PATH = os.path.join(CURRENT_DIR, "./models/classes.txt")

model = None

def load_models():
    global model
    model = load_model(MODEL_PATH)
    print("MODEL LOADED")

@app.on_event("startup")
async def startup_event():
    load_models()

def get_image_results(image_path, target_size=(150, 150)):
    image = Image.open(image_path)
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target_size)
    img_array = img_to_array(image)
    img_array = img_array.reshape(1, 150, 150, 3)

    result = model.predict(img_array)
    return result

@app.get("/")
async def hello() -> str:
    return "Hello World"

@app.post("/tomography/upload")
async def upload(file: Annotated[bytes, File()]):
    if not file.filename.endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="File format not supported.")

    file_location = f"temp_{uuid.uuid4()}.png"
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    try:
        results = get_image_results(file_location)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(file_location)

    return {"results": results.tolist()}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
