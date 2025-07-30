from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
from pathlib import Path
import json

app = FastAPI(title="🌿 Plant Recognition API", version="1.0")

INFO_PATH = Path(__file__).parent.parent / "data" / "plants_info.json"
UPLOAD_DIR = Path("api/uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

with open(INFO_PATH, "r", encoding="utf-8") as f:
    plant_info = json.load(f)

@app.get("/")
def home():
    return {
        "message": "Добро пожаловать в API определения растений!",
        "endpoints": {
            "docs": "/docs",
            "predict": "POST /predict (с фото)"
        }
    }

@app.post("/predict")
async def predict_plant(photo: UploadFile = File(...)):
    # Проверка формата
    if not photo.content_type.startswith("image/"):
        return JSONResponse(
            {"error": "Файл должен быть изображением"},
            status_code=400
        )

    file_path = UPLOAD_DIR / photo.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(photo.file, buffer)
    except Exception as e:
        return JSONResponse(
            {"error": f"Не удалось сохранить файл: {str(e)}"},
            status_code=500
        )

    # Имитация предсказания
    import random
    predicted_plant = random.choice(list(plant_info.keys()))
    info = plant_info[predicted_plant]

    return JSONResponse({
        "filename": photo.filename,
        "prediction": predicted_plant,
        "scientific_name": info["latin"],
        "family": info["family"],
        "region": info["region"],
        "season": info["season"],
        "uses": info["uses"],
        "status": "mock_mode — модель ещё обучается"
    })