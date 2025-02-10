# House Price Prediction

![House Price Prediction](https://via.placeholder.com/800x300.png?text=House+Price+Prediction)

## Overview
This is a **Machine Learning-based House Price Prediction** project that helps users estimate property prices based on various features like location, area, number of bedrooms, bathrooms, and construction status. The application is built using **Flask** and deployed on a cloud server.

### Live Demo
🖥️ **Current Deployment:** [House Price Prediction App](http://13.60.187.226:8080/)

## Features
- 📍 Predicts house prices based on key attributes
- 🏗️ Considers construction status and possession date
- 🏙️ Supports multiple cities
- 📊 Uses a trained ML model for predictions
- 🖥️ Web-based interface built with Flask

## Tech Stack
- **Backend:** Flask, Python
- **Machine Learning:** Scikit-learn, Pandas, NumPy
- **Frontend:** HTML, CSS, JavaScript
- **Deployment:** AWS EC2

## Installation
### Prerequisites
- Python 3.8+
- Virtual Environment (optional but recommended)

### Setup
```bash
# Clone the repository
git clone https://github.com/B1-86859-Assignment/Project-CDAC-.git
cd Project-CDAC

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python3 app.py
```

## Model Training
1. Load the dataset (`properties.csv`).
2. Preprocess data: handle missing values, encode categorical features.
3. Train model using **Linear Regression, Decision Trees, or Random Forest**.
4. Save the model as `model.pkl`.
5. Deploy using Flask.

## API Endpoints
- **`POST /predict`**: Accepts JSON input and returns predicted house price.

Example Request:
```json
{
    "area": 1200,
    "bhk": 3,
    "bathrooms": 2,
    "location": "Pune",
    "construction_status": "Ready to Move"
}
```

Example Response:
```json
{
    "predicted_price": 75.5 Lakh
}
```

## Deployment
The project is deployed on an **AWS EC2 instance** .

## Future Enhancements
- 🔥 Improve accuracy with advanced models (XGBoost, Neural Networks)
- 📌 Add a user authentication system
- 🌎 Expand to support international locations

## Contributors
- **Narayan Rajesh Attarde**
- **Amogh Mukunda Jaronde**


