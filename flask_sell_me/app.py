from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from torchvision import models, transforms
from PIL import Image
import torch
import os
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'

with open('imagenet-simple-labels.json') as f:
    class_idx = json.load(f)

model = models.resnet50(pretrained=True)
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/uploads')
def index():
    return render_template('uploads.html')

@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    filename = None
    classification = None
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        image = Image.open(file_path).convert('RGB')
        image = transform(image).unsqueeze(0)
        with torch.no_grad():
            outputs = model(image)
            _, predicted = torch.max(outputs, 1)
            classification = class_idx[predicted.item()]
    return render_template('prediction.html', filename=filename, classification=classification)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    image_names = os.listdir('./static/uploads')
    return render_template('dashboard.html', image_names=image_names)

if __name__ == '__main__':
    app.run(debug=True)