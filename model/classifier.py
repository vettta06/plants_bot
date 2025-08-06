from pathlib import Path

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import json
import os
import random

MODEL_PATH = Path(__file__).parent / "model.pth"
INFO_PATH = "data/plants_info.json"
CLASSES_PATH = Path(__file__).parent.parent / "data" / "classes.json"

with open(INFO_PATH, "r", encoding="utf-8") as f:
    plant_info = json.load(f)

with open(CLASSES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


plant_names = list(plant_info.keys())

def create_model(num_classes):
    model = models.resnet18(pretrained=False)
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model

num_classes = len(plant_info)
model = create_model(num_classes)
model_loaded = False

try:
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    model_loaded = True
    print("Модель загружена.")
except FileNotFoundError:
    print("Файл модели model.pth не найден. Работаю в режиме заглушки.")
except Exception as e:
    print(f"Ошибка загрузки модели: {e}. Работаю в режиме заглушки.")

def predict(image_path):
    if model_loaded:
        try:
            image = Image.open(image_path).convert("RGB")
            image_t = transform(image).unsqueeze(0)

            with torch.no_grad():
                outputs = model(image_t)
                _, predicted = torch.max(outputs, 1)
                class_idx = predicted.item()
                class_name = class_names[class_idx]

            return class_name, plant_info[class_name]["latin"]
        except Exception as e:
            print(f"Ошибка при предсказании: {e}")
            return None, None
    else:
        try:
            predicted_name = random.choice(plant_names)
            return predicted_name, plant_info[predicted_name]["latin"]
        except Exception as e:
            print(f"Ошибка в заглушке: {e}")
            return None, None