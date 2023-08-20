from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_jwt_extended import JWTManager
from flask_restful import Api

# ---- Settings ----
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy()
migrate = Migrate(app, db)
jwt = JWTManager(app)
api = Api(app)
db.init_app(app)

# ---- Views ----
from views import *

# ---- BluePrints ----
from apps.user import user
from apps.student import student

app.register_blueprint(user)
app.register_blueprint(student)
