from flask import Flask, render_template, request
import pickle
import json
import numpy as np

app = Flask(__name__)

# Load the model and scalers
with open('random_forest_best_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('area_scaler.pkl', 'rb') as scaler_file:
    area_scaler = pickle.load(scaler_file)

with open('location_mapping.json', 'r') as mapping_file:
    location_mapping = json.load(mapping_file)

@app.route('/')
def home():
    return render_template('index.html', location_mapping=location_mapping)

@app.route('/predict', methods=['POST'])
def predict():
    # Get input data from the form
    area_sqft = float(request.form['area_sqft'])
    bhk = int(request.form['bhk'])
    bathrooms = int(request.form['bathrooms'])
    construction_status = int(request.form['construction_status'])
    city = int(request.form['city'])
    location = int(request.form['location'])

    # Scale the area
    scaled_area = area_scaler.transform(np.array([[area_sqft]]))

    # Prepare the input for the model
    input_data = np.array([[scaled_area[0][0], bhk, bathrooms, construction_status, city, location]])

    # Make prediction
    predicted_price = model.predict(input_data)

    return render_template('index.html', prediction=predicted_price[0], location_mapping=location_mapping)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)
