# app.py
from flask import Flask, render_template, request
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

app = Flask(__name__)

# Load the DistilBERT model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")
model.eval()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        text = request.form['text']

        # Tokenize and preprocess the input text
        inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        
        # Make the prediction
        with torch.no_grad():
            output = model(**inputs)
        
        logits = output.logits
        probabilities = logits.softmax(dim=1)
        
        # Determine sentiment based on probabilities
        positive_prob = probabilities[0][1].item()
        negative_prob = probabilities[0][0].item()

        if positive_prob > negative_prob:
            sentiment = "Positive"
        else:
            sentiment = "Negative"

        return render_template('result.html', sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
