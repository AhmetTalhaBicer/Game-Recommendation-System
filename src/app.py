from flask import Flask
from routes.baseRoutes import init_routes


# Flask app setup
app = Flask(__name__)

# Initialize routes
init_routes(app)

if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=5000, debug=True)

# Path: src/routes/baseRoutes.py
