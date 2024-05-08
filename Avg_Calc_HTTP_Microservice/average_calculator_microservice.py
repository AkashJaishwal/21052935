from flask import Flask, jsonify
import requests
import threading
import time
from collections import deque

app = Flask(__name__)

# Constants
WINDOW_SIZE = 10
TEST_SERVER_URL = "http://20.244.56.144/test"

# Global variables
numbers_queue = deque(maxlen=WINDOW_SIZE)
lock = threading.Lock()

def fetch_numbers():
    try:
        response = requests.get(TEST_SERVER_URL)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print("Error fetching numbers from the test server:", e)
    return None

def update_numbers():
    while True:
        with lock:
            numbers = fetch_numbers()
            if numbers:
                for num in numbers:
                    if num not in numbers_queue:
                        numbers_queue.append(num)
        time.sleep(1)  # Fetch numbers every second

update_thread = threading.Thread(target=update_numbers)
update_thread.daemon = True
update_thread.start()

@app.route("/numbers/<numberid>")
def calculate_average(numberid):
    with lock:
        numbers = list(numbers_queue)
        numbers_copy = numbers.copy()
        if numberid == "p":
            numbers = [num for num in numbers if is_prime(num)]
        elif numberid == "f":
            numbers = [num for num in numbers if is_fibonacci(num)]
        elif numberid == "e":
            numbers = [num for num in numbers if num % 2 == 0]
        elif numberid == "r":
            # No filtering needed for random numbers
            pass

        window_prev_state = numbers_copy[-WINDOW_SIZE:]
        window_curr_state = list(numbers)
        avg = sum(numbers) / len(numbers) if numbers else 0

        response = {
            "numbers": numbers,
            "windowPrevState": window_prev_state,
            "windowCurrState": window_curr_state,
            "avg": avg
        }
        return jsonify(response)

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def is_fibonacci(n):
    return is_square(5 * n * n + 4) or is_square(5 * n * n - 4)

def is_square(x):
    return int(x**0.5)**2 == x

if __name__ == "__main__":
    app.run(port=9876)
