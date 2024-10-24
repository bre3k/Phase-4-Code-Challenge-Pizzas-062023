from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Create the Flask app instance
app = Flask(__name__)

# Configuring the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza_restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database object
db = SQLAlchemy(app)

# Initialize Flask-RESTful API
api = Api(app)

