from flask import Flask, request, jsonify
import requests

app = Flask(__name__)


TEST_SERVER_BASE_URL = "http://20.244.56.144/test"


@app.route('/categories/<category_name>/products', methods=['GET'])
def get_top_products(category_name):
    
    top_n = int(request.args.get('top', 10))
    min_price = request.args.get('minPrice', None)
    max_price = request.args.get('maxPrice', None)
    sort_by = request.args.get('sortBy', None)
    order = request.args.get('order', 'asc')

    
    url = f"{TEST_SERVER_BASE_URL}/companies/{category_name}/categories/{category_name}/products"
    params = {
        "top": top_n,
        "minPrice": min_price,
        "maxPrice": max_price,
        "sortBy": sort_by,
        "order": order
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        products = response.json()["products"]
        return jsonify(products), 200
    else:
        return jsonify({"error": "Failed to fetch products."}), 500


@app.route('/categories/<category_name>/products/<product_id>', methods=['GET'])
def get_product_details(category_name, product_id):
    
    url = f"{TEST_SERVER_BASE_URL}/companies/{category_name}/categories/{category_name}/products/{product_id}"
    response = requests.get(url)

    if response.status_code == 200:
        product_details = response.json()
        return jsonify(product_details), 200
    else:
        return jsonify({"error": "Failed to fetch product details."}), 500

if __name__ == '__main__':
    app.run(debug=True)
