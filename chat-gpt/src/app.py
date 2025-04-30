import random
import os

import requests
import torch
from bs4 import BeautifulSoup
from datasets import load_dataset
from flask import Flask, jsonify, request  # type: ignore
from flask_cors import CORS
from PIL import Image  # type: ignore
from sklearn.metrics.pairwise import cosine_similarity
from torchvision import models, transforms
from transformers import AutoModel, AutoTokenizer

app = Flask(__name__)
CORS(app)

# Load datasets
dataset = load_dataset("Mostafijur/Skin_disease_classify_data")
dataset1 = load_dataset("brucewayne0459/Skin_diseases_and_care")

device = torch.device('cpu')
classes = {
    0: 'Acne and Rosacea',
    1: 'Actinic Keratosis Basal Cell Carcinoma',
    2: 'Nail Fungus',
    3: 'Psoriasis Lichen Planus',
    4: 'Seborrheic Keratoses',
    5: 'Tinea Ringworm Candidiasis',
    6: 'Warts Molluscum'
}

# Load models and tokenizers
tokenizer1 = AutoTokenizer.from_pretrained("Unmeshraj/skin-disease-detection")
model1 = AutoModel.from_pretrained("Unmeshraj/skin-disease-detection")
tokenizer2 = AutoTokenizer.from_pretrained("Unmeshraj/skin-disease-treatment-plan")
model2 = AutoModel.from_pretrained("Unmeshraj/skin-disease-treatment-plan")

# Use relative path for model
model_path = os.path.join(os.path.dirname(__file__), "model.pth")
image_model = models.resnet18(pretrained=False)
image_model.fc = torch.nn.Linear(image_model.fc.in_features, len(classes))
image_model.load_state_dict(torch.load(model_path, map_location=device))
image_model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5], [0.5])
])

# Helper functions
def embed_text(text, tokenizer, model):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1)

queries, diseases, embeddings = [], [], []
for example in dataset['train']:
    query = example['Skin_disease_classification']['query']
    disease = example['Skin_disease_classification']['disease']
    queries.append(query)
    diseases.append(disease)
    query_embedding = embed_text(query, tokenizer1, model1)
    embeddings.append(query_embedding)

topics, information, topic_embeddings = [], [], []
for example in dataset1['train']:
    topic = example['Topic']
    info = example['Information']
    topics.append(topic)
    information.append(info)
    topic_embedding = embed_text(topic, tokenizer2, model2)
    topic_embeddings.append(topic_embedding)

def find_similar_disease(input_query):
    input_embedding = embed_text(input_query, tokenizer1, model1)
    similarities = [
        cosine_similarity(input_embedding.detach().numpy(), emb.detach().numpy())[0][0]
        for emb in embeddings
    ]
    return diseases[similarities.index(max(similarities))]

def format_treatment(treatment):
    formatted_treatment = treatment.replace('**', '<strong>').replace('**', '</strong>')
    lines = treatment.split('\n')
    formatted_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith('*'):
            formatted_lines.append(f'<li>{line[1:].strip()}</li>')
        elif line:
            formatted_lines.append(f'<p>{line}</p>')
    return f'<div class="formatted-treatment">{"".join(formatted_lines)}</div>'

# Placeholder treatment plans
treatment_plans = {
    "Acne and Rosacea": "* Wash your face gently twice a day\n* Avoid touching your face\n* Use recommended creams",
    "Nail Fungus": "* Use antifungal cream\n* Keep nails dry and short"
}

def find_treatment_plan(disease_name):
    return format_treatment(treatment_plans.get(disease_name, "Treatment plan not available"))

def predict_image(img):
    img_tensor = transform(img).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = image_model(img_tensor)
        _, predicted = torch.max(outputs, 1)
    return classes[predicted.item()]

def fetchDoctors(location, query, mode, backupQuery, backupMode, locality):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    # Philippine Dermatology Society directory (static fallback)
    def fetch_from_static():
        # Simulated dermatologists in Laguna from PDS directory
        return [
            {"name": "Dr. Maria Santos", "link": "https://pds.org.ph/search-dermatologist/?loc=laguna", "clinics": ["Sta Cruz Skin Center"]},
            {"name": "Dr. Jose Dela Cruz", "link": "https://pds.org.ph/search-dermatologist/?loc=laguna", "clinics": ["Laguna Dermatology Clinic"]}
        ], 200

    return fetch_from_static()[0]

@app.route('/api/ImageAi', methods=['POST'])
def image_ai():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    image = Image.open(file.stream).convert('RGB')
    predicted_disease = predict_image(image)
    treatment_plan = find_treatment_plan(predicted_disease)

    locality = "laguna"
    location = "sta cruz"
    query = predicted_disease.replace(" ", "%20")
    mode = "symptom"
    doctor_info = fetchDoctors(location, query, mode, "", "", locality)

    return jsonify({
        'result': predicted_disease,
        'treatment': treatment_plan,
        'doctors': doctor_info
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)
