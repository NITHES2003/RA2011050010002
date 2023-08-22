from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# John Doe Railways API endpoint and access token
API_BASE_URL = "http://20.244.56.144:80/train"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTI3MDk2ODQsImNvbXBhbnlOYW1lIjoiVHJhaW4gQ2VudHJhbCIsImNsaWVudElEIjoiNTI3OThjZDYtZmRhNC00NTQ0LWEzYTAtMDIwYzc0NWM3NzI1Iiwib3duZXJOYW1lIjoiIiwib3duZXJFbWFpbCI6IiIsInJvbGxObyI6IlJBMjAxMTA1MDAxMDAwMiJ9.Cv1spgxqgLarDix1its5kv7_RjsM0GauNkT21qFRcCM"

# Function to get train data from the API
def get_train_data():
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(f"{API_BASE_URL}/trains", headers=headers)
    return response.json()

# Function to process and filter trains
def process_trains(trains):
    now = datetime.now()
    allowed_time_window = timedelta(hours=12)
    filtered_trains = []

    for train in trains:
        departure_time = datetime.strptime(train["departure_time"], "%Y-%m-%d %H:%M:%S")
        delay_in_minutes = int(train["delay_minutes"])
        adjusted_departure_time = departure_time + timedelta(minutes=delay_in_minutes)

        if adjusted_departure_time > now + timedelta(minutes=30) and adjusted_departure_time <= now + allowed_time_window:
            filtered_trains.append(train)

    sorted_trains = sorted(filtered_trains, key=lambda x: (x["price"], -x["available_tickets"], -int(x["delay_minutes"])))
    return sorted_trains

@app.route("/trains", methods=["GET"])
def get_filtered_trains():
    try:
        trains_data = get_train_data()
        processed_trains = process_trains(trains_data)
        return jsonify(processed_trains)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)