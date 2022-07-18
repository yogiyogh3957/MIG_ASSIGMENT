from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
db = SQLAlchemy(app)
jwt_app = JWTManager(app)
CORS(app)

from main import routes