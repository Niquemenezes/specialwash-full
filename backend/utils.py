from .models import Usuario
# backend/utils.py

from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
import json

def verificar_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            return jsonify({"msg": "Token inválido", "error": str(e)}), 401
        return f(*args, **kwargs)
    return decorator

def normalizar_rol(rol):
    return rol.lower().strip()
