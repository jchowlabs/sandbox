import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Load the shoe size and cost dataset into a Pandas dataframe
shoe_data = pd.read_csv('shoepriceonly.csv')

# Split the dataset into features (shoe size) and target (shoe cost)
X = shoe_data.iloc[:, :-1].values
y = shoe_data.iloc[:, 1].values

# Create a Linear Regression model and fit it to the data
model = LinearRegression()
model.fit(X, y)

# Pickle the model and save it to Google Drive
filename = '/content/drive/My Drive/model.pkl'
pickle.dump(model, open(filename, 'wb'))

# Testing
#model = pickle.load(open('model.pkl','rb'))
#shoe_sizes = [8, 9, 10, 11, 20] # Example shoe sizes
#for size in shoe_sizes:
  #print(model.predict([[size]]))