import requests

def get_all_products():
    response = requests.get('http://127.0.0.1:5000/products')
    data = response.json()
    return data

def get_product(product_id):
    response = requests.get(f'http://127.0.0.1:5000/products/{product_id}')
    data = response.json()
    return data

def add_product(name):
    new_product = {"name": name}
    response = requests.post('http://127.0.0.1:5000/products', json=new_product)
    data = response.json()
    return data

if __name__ == '__main__':
    all_products = get_all_products()
    print("All Products:")
    print(all_products)

    product_1 = get_product(1)
    print(f"\nSpecified Product:")
    print(product_1)

    new_product = add_product("Salt")
    print(f"\nAdding New Product:")
    print(new_product)
