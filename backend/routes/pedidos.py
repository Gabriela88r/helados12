from flask import Blueprint, request, jsonify
from db import pedidos
from bson.objectid import ObjectId

import smtplib
from email.mime.text import MIMEText
from flask import session

from config import EMAIL_USER, EMAIL_PASS, EMAIL_TO

pedidos_bp = Blueprint("pedidos", __name__)


# 🔥 CREAR PEDIDO
@pedidos_bp.route("/", methods=["POST"])
def crear_pedido():

    data = request.json

    # Estado inicial
    data["estado"] = "pendiente"

    # Guardar
    pedidos.insert_one(data)

    # ✉️ Email
    mensaje = "Nuevo pedido:\n\n"

    for p in data["productos"]:

        mensaje += (
            f"{p['nombre']} "
            f"x{p['cantidad']} "
            f"- ₡{p['precio']}\n"
        )

    mensaje += f"\nTotal: ₡{data['total']}"

    msg = MIMEText(mensaje)

    msg["Subject"] = "Nuevo Pedido"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    try:

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(EMAIL_USER, EMAIL_PASS)

        server.send_message(msg)

        server.quit()

    except Exception as e:

        print("Error correo:", e)

    return jsonify({
        "msg": "Pedido guardado"
    })


# 🔥 OBTENER PEDIDOS
@pedidos_bp.route("/", methods=["GET"])
def obtener_pedidos():

    lista = []

    for p in pedidos.find():

        p["_id"] = str(p.get("_id"))

        lista.append(p)

    return jsonify(lista)


# 🔥 FINALIZAR PEDIDO
@pedidos_bp.route("/finalizar/<id>", methods=["PUT"])
def finalizar_pedido(id):

    pedidos.update_one(
        {"_id": ObjectId(id)},
        {
            "$set": {
                "estado": "finalizado"
            }
        }
    )

    return jsonify({
        "msg": "Pedido finalizado"
    })


@pedidos_bp.route("/eliminar/<id>", methods=["DELETE"])
def eliminar_pedido(id):

    pedidos.delete_one({
        "_id": ObjectId(id)
    })

    return jsonify({
        "msg": "Pedido eliminado"
    })
