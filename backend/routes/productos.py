from flask import Blueprint, jsonify, request
from db import productos
from bson import ObjectId

productos_bp = Blueprint("productos", __name__)

# 🔥 OBTENER PRODUCTOS


@productos_bp.route("/", methods=["GET"])
def obtener_productos():

    lista = []

    for p in productos.find():

        lista.append({
            "id": str(p["_id"]),
            "nombre": p.get("nombre"),
            "precio": p.get("precio"),
            "img": p.get("img", "")
        })

    return jsonify(lista)

# 🔥 CREAR PRODUCTO


@productos_bp.route("/", methods=["POST"])
def crear_producto():

    data = request.json

    resultado = productos.insert_one(data)

    return jsonify({
        "msg": "Producto creado",
        "id": str(resultado.inserted_id)
    })

# 🔥 ELIMINAR


@productos_bp.route("/<id>", methods=["DELETE"])
def eliminar_producto(id):

    productos.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "msg": "Producto eliminado"
    })
