from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask application and the database
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import models

from app.routes.auth_routes import auth_routes
from app.routes.technical_analyses_routes import technical_analyses_routes
from app.routes.fundamental_analysis_routes import fundamental_analysis_routes

app.register_blueprint(auth_routes, url_prefix='/api')
app.register_blueprint(technical_analyses_routes, url_prefix='/api')
app.register_blueprint(fundamental_analysis_routes, url_prefix='/api')