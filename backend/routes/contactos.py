from flask import Blueprint, request, jsonify
from db import contactos

contactos_bp = Blueprint("contactos", __name__)


@contactos_bp.route("/", methods=["POST"])
def contacto():
    data = request.json
    contactos.insert_one(data)
    return jsonify({"msg": "Mensaje enviado"})
