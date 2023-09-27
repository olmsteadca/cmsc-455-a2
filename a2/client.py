import requests
from flask import Flask

app = Flask(__name__)

# ProductService methods
def get_products():
    response = requests.get('http://127.0.0.1:5000/products')
    if response.status_code == 200:
        data = response.json()
        print("All Products in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}:")
        print(response.json())

def get_product(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    if response.status_code == 200:
        data = response.json()
        print(f"Product {product_id} in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())

def add_product(name):
    new_product = {"name": name}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    if response.status_code == 200:
        data = response.json()
        print("New Product in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())

def remove_product(product_id):
    response = requests.post(f'http://127.0.0.1:5000/products/{product_id}')
    if response.status_code == 200:
        data = response.json()
        print("Removed Product from Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.json())

def remove_products():
    response = requests.post('http://127.0.0.1:5000/products/edit')
    if response.status_code == 200:
        data = response.json()
        print("Removed Products from Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")

# CartService methods
def get_products_in_cart(user_id):
    response = requests.get(f'http://127.0.0.1:5000/cart/{user_id}')
    if response.status_code == 200:
        data = response.json()
        print("Products in Cart:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def add_product_to_cart(user_id, product_id):
    product = {"product_id" : product_id}
    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}/add/{product_id}', json=product)
    if response.status_code == 200:
        data = response.json()
        print("Added Product to Cart:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def remove_product_from_cart(user_id, product_id, quantity):
    quantity = {"quantity" : quantity}
    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}/remove/{product_id}', json=quantity)
    if response.status_code == 200:
        data = response.json()
        print("Removed Product from Cart:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def add_user(username):
    new_user = {"username" : username}
    response = requests.post(f'http://127.0.0.1:5000/users', json=new_user)
    if response.status_code == 200:
        data = response.json()
        print("User Added:")
        print(data)
    elif response.status_code == 400:
        data = response.json()
        print("Error Encountered:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")


if __name__ == '__main__':
    '''new_products = {"Salt", "Pepper", "Strawberries", "Laundry Detergent", "Formula", "2% Milk", "Almond Milk", "CheezIts"}
    for product in new_products:
        add_product(product)
        print()
    get_products()'''

    add_user("olmsteadca")
    print()
    user_id = 1
    product1 = 3
    product2 = 1

    add_product_to_cart(user_id, product1)
    print()
    add_product_to_cart(user_id, product1)
    print()
    add_product_to_cart(user_id, product2)
    print()

    remove_product_from_cart(user_id, product1, 1)
    print()

    get_products_in_cart(user_id)



    
