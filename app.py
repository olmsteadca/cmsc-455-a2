from ProductService import app as ProductService_app
from CartService import app as CartService_app
from client import app as client_app
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Assignment2: All services are running."

if __name__ == '__main__':
    app.run()
