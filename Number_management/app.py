from flask import Flask, request, jsonify
import requests
import concurrent.futures
from urllib.parse import urlparse

app = Flask(__name__)

# Function to fetch numbers from a URL
def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json().get('numbers', [])
    except requests.Timeout:
        pass
    return []

# Function to merge and sort unique numbers
def merge_and_sort_numbers(number_lists):
    merged_numbers = set()
    for numbers in number_lists:
        merged_numbers.update(numbers)
    return sorted(merged_numbers)

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    number_lists = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_numbers, url) for url in urls]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                number_lists.append(result)

    merged_numbers = merge_and_sort_numbers(number_lists)
    return jsonify({'numbers': merged_numbers})

if __name__ == '__main__':
    app.run(host='localhost', port=13000)

