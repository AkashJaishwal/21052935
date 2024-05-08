import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Add your authorization header token here
auth_header = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiZXhwIjoxNzE1MTUwOTY1LCJpYXQiOjE3MTUxNTA2NjUsImlzcyI6IkFmZm9yZG1lZCIsImp0aSI6Ijg4ZDAzMjlmLTNkY2UtNDEzNS05MWY1LTliMzAyNmQ2ZjhlZSIsInN1YiI6ImFrYXNoamFpc3dhbDMzNEBnbWFpbC5jb20ifSwiY29tcGFueU5hbWUiOiJqYWlTb2xuIiwiY2xpZW50SUQiOiI4OGQwMzI5Zi0zZGNlLTQxMzUtOTFmNS05YjMwMjZkNmY4ZWUiLCJjbGllbnRTZWNyZXQiOiJLUlVuWHZ1Z296U3dkeFpnIiwib3duZXJOYW1lIjoiQWthc2giLCJvd25lckVtYWlsIjoiYWthc2hqYWlzd2FsMzM0QGdtYWlsLmNvbSIsInJvbGxObyI6IjIxMDUyOTM1In0.i2RwMVr_7RcPti2sCu5nBQTzxqbtAK6OidS6Ep0wngs'
}

@app.route('/categories/<string:categoryname>/products', methods=['GET'])
def get_top_products(categoryname):
    n = int(request.args.get('n', 10))
    page = int(request.args.get('page', 1))
    sort_by = request.args.get('sortBy', 'rating')
    sort_order = request.args.get('sortOrder', 'desc')
    min_price = request.args.get('minPrice', None)
    max_price = request.args.get('maxPrice', None)

    companies = ['AMZ', 'FLP', 'SNP', 'MYN', 'AZO']
    products = []

    for company in companies:
        url = f'http://20.244.56.144/test/companies/{company}/categories/{categoryname}/products'
        params = {
            'top': n,
            'minPrice': min_price,
            'maxPrice': max_price
        }
        response = requests.get(url, params=params, headers=auth_header)
        data = response.json()
        products.extend(data['products'])

    # Sorting
    products.sort(key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))

    # Pagination
    start_index = (page - 1) * n
    end_index = start_index + n
    products = products[start_index:end_index]

    # Custom unique ID
    for product in products:
        product['id'] = f'{categoryname}-{product["company"]}-{product["name"]}-{product["price"]}'

    total_products = len(products)
    total_pages = (total_products - 1) // n + 1

    return jsonify({
        'products': products,
        'totalProducts': total_products,
        'totalPages': total_pages
    })

@app.route('/categories/<string:categoryname>/products/<string:productid>', methods=['GET'])
def get_product_details(categoryname, productid):
    products = [
        {
            "id": "1234567890",
            "name": "Product Name",
            "company": "Company Name",
            "category": "Category Name",
            "price": 123.45,
            "rating": 4.5,
            "discount": 10
        },
        # ... more products
    ]

    product = next((p for p in products if p['id'] == productid), None)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)