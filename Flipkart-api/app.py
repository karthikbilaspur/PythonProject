from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Flipkart API credentials
client_id = "your_client_id"
client_secret = "your_client_secret"

# Get access token
def get_access_token():
    url = "https://api.flipkart.net/oauth-service/oauth/token"
    params = {"grant_type": "client_credentials", "scope": "Seller_Api"}
    headers = {"Authorization": f"Basic {get_base64_encoded_string()}"}
    response = requests.get(url, params=params, headers=headers)
    return response.json()["access_token"]

# Get base64 encoded string
def get_base64_encoded_string():
    import base64
    return base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

# Get products
def get_products():
    url = "https://api.flipkart.net/sellers/v3/products"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Get orders
def get_orders():
    url = "https://api.flipkart.net/sellers/v3/orders"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    response = requests.get(url, headers=headers)
    return response.json()

# Update inventory
def update_inventory(sku_id, quantity):
    url = f"https://api.flipkart.net/sellers/skus/{sku_id}/listings"
    headers = {"Authorization": f"Bearer {get_access_token()}"}
    data = {"attributeValues": {"inventory": quantity}}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def products():
    products = get_products()
    return render_template("products.html", products=products)

@app.route("/orders")
def orders():
    orders = get_orders()
    return render_template("orders.html", orders=orders)

@app.route("/inventory", methods=["POST"])
def inventory():
    sku_id = request.form["sku_id"]
    quantity = request.form["quantity"]
    update_inventory(sku_id, quantity)
    return jsonify({"message": "Inventory updated successfully"})

@app.route("/products/filter", methods=["GET"])
def filter_products():
    category = request.args.get("category")
    price_min = request.args.get("price_min")
    price_max = request.args.get("price_max")
    # Filter products based on category, price range, and other criteria
    products = get_products()
    filtered_products = [product for product in products if product["category"] == category and product["price"] >= int(price_min) and product["price"] <= int(price_max)]
    return jsonify(filtered_products)

@app.route("/orders/filter", methods=["GET"])
def filter_orders():
    status = request.args.get("status")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    # Filter orders based on status, date range, and other criteria
    orders = get_orders()
    filtered_orders = [order for order in orders if order["status"] == status and order["date"] >= date_from and order["date"] <= date_to]
    return jsonify(filtered_orders)

if __name__ == "__main__":
    app.run(debug=True)