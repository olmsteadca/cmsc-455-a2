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

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    cart = db.relationship('Cart', backref='user', lazy=True)

# Endpoint 1: Get list of grocery products in a user's cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_products(user_id):
    user = User.query.get(user_id)
    product_list = []

    for item in user.cart:
        product = Product.query.get(item.product_id)
        product_list.append({
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "quantity": product.quantity
        })
    return jsonify({"products": product_list})

# Endpoint 2: Add a new product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_product(user_id, product_id):
    data = request.json
    cart = User.query.get(user_id).cart
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found in grocery store"}), 404

    if "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    existing_product = cart.query.get(product_id)

    if existing_product:
        existing_product.quantity += 1
        db.session.commit()
        return jsonify({"message": "Quantity updated", "product": {
            "id": existing_product.id, 
            "name": existing_product.name,
            "price": existing_product.price, 
            "quantity": existing_product.quantity
        }})
    
    else:
        new_product = Cart(user_id=user_id, product_id=product_id)
        if new_product:
            db.session.add(new_product)
            product.quantity -= 1
            db.session.commit()
            return jsonify({
                "message": "Product added to cart",
                "product": {
                    "id": new_product.id, 
                    "name": new_product.name,
                    "price": new_product.price, 
                    "quantity": new_product.quantity
                },
                "message": "Store quantity updated",
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity
                }
            })

# Endpoint 3: Delete a specified quantity of a product in a user's cart by ID
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_product(user_id, product_id, quantity_removed):
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found in grocery store"}), 404

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()

    if cart_item:
        if cart_item.quantity <= quantity_removed:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({
                "message": "Product removed from cart",
                "product": {
                    "id": product.id, 
                    "name": product.name,
                    "price": product.price, 
                    "quantity": product.quantity 
                }
            })
        
        else:
            cart_item.quantity -= quantity_removed
            store_product = Product.query.get(product_id)
            store_product.quantity += quantity_removed
            db.session.commit()
            return jsonify({
                "message": "Quantity in cart updated",
                "product": {
                    "id": product.id, 
                    "name": product.name,
                    "price": product.price, 
                    "quantity": product.quantity 
                },
                "message": "Store quantity updated",
                "product": {
                    "id": store_product.id,
                    "name": store_product.name,
                    "price": store_product.price,
                    "quantity": store_product.quantity
                }
            })

    else:
        return jsonify({"error": "Product not found in user's cart"}), 404

# Endpoint 4: Adding a user
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json()

    if "username" not in data:
        return jsonify({"error" : "Username is required"}), 400
    
    existing_user = User.query.filter_by(username=data['username']).first()

    if existing_user:
        return jsonify({"error" : "Username already exists"}), 400
    
    else:
        new_user = User(username=data['username'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message" : "User added",
            "user": {
                "id": new_user.id,
                "username": new_user.username
            }
        })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
