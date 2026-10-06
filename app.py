from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib

app = Flask(__name__)
CORS(app)

# Load trained model
model = joblib.load("sales_model.pkl")

# Temporary storage for users
users = []


# HOME ROUTE
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Sales Prediction API Running"
    })


# REGISTER ROUTE
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    # Check if user already exists
    for user in users:
        if user["email"] == email:
            return jsonify({
                "message": "User already exists"
            }), 400

    users.append({
        "email": email,
        "password": password
    })

    print("Users after registration:")
    print(users)

    return jsonify({
        "message": "Registration Successful"
    })


# LOGIN ROUTE
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    print("Current users:")
    print(users)

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({
                "message": "Login Successful"
            })

    return jsonify({
        "message": "Invalid Credentials"
    }), 401


# PREDICT ROUTE
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    price = float(data["price"])
    quantity = float(data["quantity"])
    discount = float(data["discount_percentage"])
    tax = float(data["tax"])

    features = np.array([
        [price, quantity, discount, tax]
    ])

    prediction = model.predict(features)

    return jsonify({
        "predicted_total_amount": float(prediction[0])
    })


# RUN SERVER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)