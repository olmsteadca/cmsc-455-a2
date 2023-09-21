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
    quantity = db.Column(db.Integer, default=1)

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart = db.relationship('Cart', backref='user', lazy=True)

# Endpoint 1: Get list of grocery products in a user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_products():
    user = User.query.all()
    product_list = []

    for item in user.cart:
        product = Product.query.get(item.product_id)
        product_list.append({"id" : product.id, "name" : product.name, "price" : product.price, "quantity" : product.quantity})
    return jsonify({"products": product_list})

# Endpoint 2: Add a new product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_product():
    data = request.json

    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_product = Product(name=data['title'], done=False)
    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product added", "product": {"id": new_product.id, "name": new_product.name, "price": new_product.price, "quantity" : new_product.quantity}}), 201

# Endpoint 3: Delete a specified quantity of a product in a user's cart by ID
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def remove_product(quantity_removed):
    product = Product.query.get()
    if product:
        if product.quantity <= quantity_removed:
            db.session.delete(product)
            db.session.commit()
            return jsonify({"message" : "Product removed", "product" : {"id" : product.id, "name" : product.name, "price" : product.price, "quantity" : product.quantity}})
        else:
            product.quantity -= quantity_removed
            db.session.commit()
            return jsonify({"message" : "Quantity updated", "product" : {"id" : product.id, "name" : product.name, "price" : product.price, "quantity" : product.quantity}})
    else:
        return jsonify({"error": "Product not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)