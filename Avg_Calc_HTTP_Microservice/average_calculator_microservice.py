from flask import Flask, request, jsonify
import requests
from collections import deque
import time

app = Flask(__name__)

WINDOW_SIZE = 10
window = deque(maxlen=WINDOW_SIZE)
avg = 0.0


def fetch_numbers(number_type):
    url = f"http://20.244.56.144/test/{number_type}"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE1MTUwOTY1LCJpYXQiOjE3MTUxNTA2NjUsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6Ijg4ZDAzMjlmLTNkY2UtNDEzNS05MWY1LTliMzAyNmQ2ZjhlZSIsInN1YiI6ImFrYXNoamFpc3dhbDMzNEBnbWFpbC5jb20ifSwiY29tcGFueU5hbWUiOiJqYWlTb2xuIiwiY2xpZW50SUQiOiI4OGQwMzI5Zi0zZGNlLTQxMzUtOTFmNS05YjMwMjZkNmY4ZWUiLCJjbGllbnRTZWNyZXQiOiJLUlVuWHZ1Z296U3dkeFpnIiwib3duZXJOYW1lIjoiQWthc2giLCJvd25lckVtYWlsIjoiYWthc2hqYWlzd2FsMzM0QGdtYWlsLmNvbSIsInJvbGxObyI6IjIxMDUyOTM1In0.i2RwMVr_7RcPti2sCu5nBQTzxqbtAK6OidS6Ep0wngs"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["numbers"]
    else:
        return None


def calculate_avg():
    if len(window) == 0:
        return 0.0
    return sum(window) / len(window)


@app.route('/numbers/<number_type>', methods=['GET'])
def get_numbers(number_type):
    global window
    global avg

    start_time = time.time()

    
    numbers = fetch_numbers(number_type)

    if numbers is None:
        return jsonify({"error": "Failed to fetch numbers from the test server."}), 500

    
    window.extend(numbers)

    
    avg = calculate_avg()

    
    response_data = {
        "numbers": numbers,
        "windowPrevState": list(window)[-len(numbers)-1:-1],
        "windowCurrState": list(window)[-len(numbers):],
        "avg": avg
    }

    
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        return jsonify({"error": "Response time exceeded 500 milliseconds."}), 500

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='localhost', port=9876)
