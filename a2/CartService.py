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
        cart_quantity = Cart.query.filter_by(user_id=user_id, product_id=item.product_id).first().quantity
        product_list.append({
            "id": product.id, 
            "name": product.name, 
            "price": product.price, 
            "quantity": cart_quantity
        })
    return jsonify({"products": product_list})

# Endpoint 2: Add a new product to a user's cart
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_product(user_id, product_id):
    data = request.json

    if "product_id" not in data:
        return jsonify({"error" : "Product ID is required"}), 400
    
    product_id = data['product_id']
    product = Product.query.get(product_id)

    if not product:
        return jsonify({"error": "Product not found in grocery store"}), 404

    cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    

    if cart_item:
        cart_item.quantity += 1
        cart_quantity = cart_item.quantity
        product.quantity -= 1
        db.session.commit()
        return jsonify({"message": "Quantity updated", "product": {
            "id": product.id, 
            "name": product.name,
            "price": product.price, 
            "quantity": cart_quantity
        }, "store_message": "Store quantity updated", "store_product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
        }})
    
    else:
        new_product = Cart(user_id=user_id, product_id=product_id, quantity=1)
        if new_product:
            db.session.add(new_product)
            cart_quantity = new_product.quantity
            product.quantity -= 1
            db.session.commit()
            
            return jsonify({
                "message": "Product added to cart",
                "product": {
                    "id": product.id, 
                    "name": product.name,
                    "price": product.price, 
                    "quantity": cart_quantity
                },
                "store_message": "Store quantity updated",
                "store_product": {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price,
                    "quantity": product.quantity
                }
            })
        
        else:
            return jsonify({"error": "Failed to add product to cart"}), 500

# Endpoint 3: Delete a specified quantity of a product in a user's cart by ID
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_product(user_id, product_id):
    data = request.json
    quantity_removed = data['quantity']

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
    data = request.json

    if "username" not in data:
        return jsonify({"error" : "Username is required"}), 400
    
    existing_user = User.query.filter_by(username=data['username']).first()

    if existing_user:
        return jsonify({"error" : "Attempted to add a user that already exists"}), 400
    
    else:
        new_user = User(username=data['username'])
        print("username:")
        print(new_user.username)

        db.session.add(new_user)
        db.session.commit()
        print("reached commit")
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
