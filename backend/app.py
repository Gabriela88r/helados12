from flask import Flask, render_template
from flask_cors import CORS

from routes.contactos import contactos_bp
from routes.pedidos import pedidos_bp
from routes.productos import productos_bp
from routes.auth import auth_bp
from flask import session, redirect

print("🚀 INICIANDO SERVIDOR...")

app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static"
)

app.secret_key = "supersecret"

CORS(app)

# APIs
app.register_blueprint(productos_bp, url_prefix="/api/productos")
app.register_blueprint(pedidos_bp, url_prefix="/api/pedidos")
app.register_blueprint(contactos_bp, url_prefix="/api/contacto")
app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Páginas


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/pedidos")
def pedidos_page():

    if not session.get("admin"):
        return redirect("/admin")

    return render_template("pedidos.html")


if __name__ == "__main__":
    app.run(debug=False)
