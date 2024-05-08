from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

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
        response = requests.get(url, params=params)
        data = response.json()
        products.extend(data['products'])

    
    products.sort(key=lambda x: x[sort_by], reverse=(sort_order == 'desc'))

    
    start_index = (page - 1) * n
    end_index = start_index + n
    products = products[start_index:end_index]

    
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
        
    ]

    product = next((p for p in products if p['id'] == productid), None)

    if not product:
        return jsonify({'error': 'Product not found'}), 404

    return jsonify(product)

if __name__ == '__main__':
    app.run(debug=True)