import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import scipy.io
import json
import os

LABELS_FILE = "data/flowers/imagelabels.mat"
CAT_TO_NAME = "data/cat_to_name.json"

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

with open(CAT_TO_NAME, 'r', encoding='utf-8') as f:
    cat_to_name = json.load(f)

def create_model():
    model = models.resnet18(pretrained=True)
    model.fc = nn.Linear(model.fc.in_features, 102)

    return model

model = create_model()
model.eval()

def predict(image_path):
    try:
        image = Image.open(image_path).convert("RGB")
        image_t = transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = model(image_t)
            _, predicted = torch.max(outputs, 1)
            class_id = str(predicted.item() + 1)

        common_name = cat_to_name.get(class_id, "неизвестный цветок")
        scientific_name = f"Species_{class_id}"
        return common_name, scientific_name
    except Exception as e:
        print(f"Ошибка при предсказании: {e}")
        return "не удалось распознать", None