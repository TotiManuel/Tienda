from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import Usuario

# 🔴 ESTA LÍNEA ES OBLIGATORIA
auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nombre = request.form.get("usuario")
        password = request.form.get("password")

        if not nombre or not password:
            flash("Formulario incompleto", "error")
            return render_template("login.html")

        usuario = Usuario.query.filter_by(nombre=nombre).first()

        if usuario and usuario.check_password(password):
            session["usuario"] = {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "rol": usuario.rol
            }
            return redirect(url_for("web.home"))

        flash("Usuario o contraseña incorrectos", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("web.home"))
