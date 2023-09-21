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
    price = db.Column(db.Double, default=0)
    quantity = db.Column(db.Integer, default=0)

# Endpoint 1: Get list of available grocery products
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{"id": product.id, "name": product.name, "price": product.price, "quantity" : product.quantity} for product in products]
    return jsonify({"products": product_list})

# Endpoint 2: Get a specific product description by ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(task_id):
    product = Product.query.get(task_id)
    if product:
        return jsonify({"product": {"id": product.id, "name": product.name, "price": product.price, "quantity" : product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404

# Endpoint 3: Add a new product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json

    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_product = Product(name=data['title'], done=False)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added", "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price, "quantity" : new_product.quantity}}), 201

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)