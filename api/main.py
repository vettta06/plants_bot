from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path

app = FastAPI(title="🌿 Plant Recognition API", version="1.0")

UPLOAD_DIR = Path("api/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

PLANT_NAMES = ["берёза", "дуб", "крапива", "мать-и-мачеха", "одуванчик", "роза"]

@app.post("/predict")
async def predict_plant(photo: UploadFile = File(...)):
    # Сохраняем фото
    file_path = UPLOAD_DIR / photo.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)

    import random
    predicted_plant = random.choice(PLANT_NAMES)

    return JSONResponse({
        "filename": photo.filename,
        "prediction": predicted_plant,
        "scientific_name": "Species dummy",
        "info": "Это тестовый ответ. Модель ещё не подключена."
    })