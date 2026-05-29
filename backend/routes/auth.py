from flask import Blueprint, request, jsonify, session

auth_bp = Blueprint("auth", __name__)

ADMIN_USER = "admin"
ADMIN_PASS = "1234"


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if (
        data.get("user") == ADMIN_USER and
        data.get("pass") == ADMIN_PASS
    ):

        session["admin"] = True

        return jsonify({
            "msg": "Login correcto"
        })

    return jsonify({
        "error": "Credenciales incorrectas"
    }), 401
