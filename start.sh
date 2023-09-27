#!/bin/bash

# Start the Product Service on port 5000
gunicorn ProductService:app --bind 0.0.0.0:5000 &

# Start the Cart Service on port 5001
gunicorn CartService:app --bind 0.0.0.0:5001 &

# Start the Client Service on port 5002
gunicorn client:app --bind 0.0.0.0:5002

# Keep the script running to keep the services running
tail -f /dev/null
