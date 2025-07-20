from flask import Blueprint, request, jsonify
from .app import db
from .models import Usuario
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .utils import verificar_token, normalizar_rol

import json

api_bp = Blueprint('api', __name__)

@api_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    if Usuario.query.filter_by(email=data["email"]).first():
        return jsonify({"msg": "Usuario ya existe"}), 400

    nuevo = Usuario(
        nombre=data["nombre"],
        email=data["email"],
        rol=data["rol"]
    )
    nuevo.set_password(data["password"])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"msg": "Usuario creado correctamente"}), 201

@api_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = Usuario.query.filter_by(email=data["email"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"msg": "Credenciales incorrectas"}), 401

    access_token = create_access_token(identity=json.dumps({
        "id": user.id,
        "email": user.email,
        "rol": user.rol
    }))
    return jsonify({"token": access_token, "user": user.serialize()}), 200

@api_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def get_usuarios():
    return jsonify([u.serialize() for u in Usuario.query.all()])
