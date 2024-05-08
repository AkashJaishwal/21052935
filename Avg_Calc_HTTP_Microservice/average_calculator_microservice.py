from flask import Flask, request, jsonify
import requests
import time
import random

app = Flask(__name__)

window_size = 10
window_numbers = []
last_request_time = time.time()  

def fetch_numbers(endpoint):
    global last_request_time
    if time.time() - last_request_time > 0.5:
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                numbers = response.json()
                last_request_time = time.time()  
                return numbers
            else:
                print("Error: Failed to fetch numbers. Status code:", response.status_code)
        except Exception as e:
            print("Error fetching numbers:", e)
    return []

def update_window_numbers(new_number):
    global window_numbers
    if len(window_numbers) >= window_size:
        window_numbers.pop(0)
    window_numbers.append(new_number)

def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    return sum(numbers) / len(numbers)

@app.route("/numbers/<numberid>")
def process_number_request(numberid):
    global window_numbers

    if numberid == "r":
        endpoint = "http://20.244.56.144/test/rand"
    elif numberid == "p":
        endpoint = "http://20.244.56.144/test/prime"
    elif numberid == "e":
        endpoint = "http://20.244.56.144/test/even"
    else:
        return "Invalid numberid", 400

    numbers = fetch_numbers(endpoint)

    if numbers:
        
        numbers = [int(num) for num in numbers]

        for num in numbers:
            update_window_numbers(num)

    avg = calculate_average(window_numbers)

    response = {
        "numbers": numbers,
        "windowPrevState": window_numbers[:-len(numbers)],
        "windowCurrState": window_numbers,
        "avg": "{:.2f}".format(avg)
    }

    return jsonify(response)

if __name__ == "_main_":
    app.run(debug=True)