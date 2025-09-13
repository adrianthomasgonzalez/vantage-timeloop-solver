#!/bin/bash
# Tell Azure how to run your Flask app using gunicorn

# Install gunicorn if not already in requirements
pip install gunicorn

# Start the app
gunicorn --bind 0.0.0.0:$PORT app:app
