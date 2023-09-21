import requests

# ProductService methods
def get_products():
    response = requests.get('http://127.0.0.1:5000/products')
    if response.status_code == 200:
        data = response.json()
        print("All Products in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}:")

def get_product(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    if response.status_code == 200:
        data = response.json()
        print(f"Product {product_id} in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def add_product(name):
    new_product = {"name": name}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    if response.status_code == 200:
        data = response.json()
        print("New Product in Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def remove_product(product_id):
    response = requests.post(f'http://127.0.0.1:5000/products/{product_id}')
    if response.status_code == 200:
        data = response.json()
        print("Removed Product from Store:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

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
    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}')
    if response.status_code == 200:
        data = response.json()
        print("Products in Cart:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def add_product_to_cart(user_id, product_id):
    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}/add/{product_id}')
    if response.status_code == 200:
        data = response.json()
        print("Added Product to Cart:")
        print(data)
    else:
        print(f"Request failed with status code {response.status_code}")

def remove_product_from_cart(user_id, product_id, quantity):
    response = requests.post(f'http://127.0.0.1:5000/cart/{user_id}/remove/{product_id}')
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
    else:
        print(f"Request failed with status code {response.status_code}")

    

if __name__ == '__main__':
    new_products = {"Salt", "Pepper", "Strawberries", "Laundry Detergent", "Formula", "2% Milk", "Almond Milk", "CheezIts"}
    for product in new_products:
        add_product(product)
        print()
    get_products()

    add_user("olmasteadca")



    
