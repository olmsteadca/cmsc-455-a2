import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, default=0)
    quantity = db.Column(db.Integer, default=50)

# Endpoint 1: Get list of available grocery products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = []

    if products:
        for product in products:
            product_list.append({
                "id": product.id, 
                "name": product.name, 
                "price": product.price, 
                "quantity": product.quantity
            })
        return jsonify(product_list)
    else: 
        return jsonify({"error": "No products found"}), 404

# Endpoint 2: Get a specific product description by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)

    if product:
        return jsonify({"product": {
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "quantity": product.quantity
        }})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    products = Product.query.all()
    exists = False
    id = 0

    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    for product in products:
        if product.name == data['name']:
            exists = True
            id = product.id
    
    if exists:
        existing_product = Product.query.get(id)
        existing_product.quantity += 1
        db.session.commit()
        return jsonify({"message": "Quantity updated", "product": {
            "id": existing_product.id, 
            "name": existing_product.name,
            "price": existing_product.price, 
            "quantity": existing_product.quantity
        }})
    
    else:
        new_product = Product(name=data['name'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"message": "Product added", "product": {
            "id": new_product.id, 
            "name": new_product.name,
            "price": new_product.price, 
            "quantity": new_product.quantity
        }})

# Endpoint 4: Remove a product by ID
@app.route('/products/<int:product_id>', methods=['POST'])
def remove_product(product_id):
    product = Product.query.get(product_id)

    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "Product removed", "product": {
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "quantity": product.quantity
        }})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 5: Remove all products
@app.route('/products/edit', methods=['POST'])
def remove_products():
    products = Product.query.all()

    if products:
        for product in products:
            db.session.delete(product)
        db.session.commit()
        return jsonify({"message": "All products removed"})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5002, debug=True)
