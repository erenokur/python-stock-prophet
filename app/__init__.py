from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask application and the database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import the routes and models at the end to avoid circular imports
from app import routes, models

# Import the api_routes after the routes and models to avoid circular imports
from app.routes import api_routes
app.register_blueprint(api_routes, url_prefix='/api')