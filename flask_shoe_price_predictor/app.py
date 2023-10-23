import numpy as np
from flask import Flask, request, render_template
import pickle

# name of app
app = Flask(__name__)

# loading saved model as model
model = pickle.load(open('models/model.pkl', 'rb'))

# decorator
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

    # gets input from user and formats before processing
    int_features = [float(x) for x in request.form.values()] 
    features = [np.array(int_features)]  
    prediction = model.predict(features)  
    output = round(prediction[0], 2)

    # outputs prediction on index.html page
    return render_template('index.html', prediction_text='Price Prediction: ${}'.format(output))

if __name__ == "__main__":
    app.run()
