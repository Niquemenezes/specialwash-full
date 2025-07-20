from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar variables del entorno
load_dotenv()

# Base de datos
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    # Inicializar extensiones
    CORS(app)
    db.init_app(app)
    jwt.init_app(app)

    # Registrar blueprints
    from .api import api_bp   # <- CORREGIDO con punto
    app.register_blueprint(api_bp, url_prefix="/api")

    return app

# Para usar flask run
app = create_app()
