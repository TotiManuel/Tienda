from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from models import Usuario, Venta, db

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")

def login_requerido():
    if "usuario" not in session or session["usuario"]["rol"] != "cliente":
        return False
    return True

@cliente_bp.route("/pedidos")
def pedidos():
    if not login_requerido():
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario"]["id"]

    pedidos = (
        Venta.query
        .filter_by(usuario_id=usuario_id)
        .order_by(Venta.fecha.desc())
        .all()
    )

    return render_template(
        "cliente/pedidos.html",
        pedidos=pedidos
    )

@cliente_bp.route("/perfil", methods=["GET", "POST"])
def perfil():
    if not login_requerido():
        return redirect(url_for("auth.login"))

    usuario_id = session["usuario"]["id"]
    usuario = Usuario.query.get_or_404(usuario_id)

    if request.method == "POST":
        nombre = request.form.get("nombre").strip()
        password = request.form.get("password")

        # Validar nombre
        if not nombre:
            flash("El nombre no puede estar vacío", "error")
            return redirect(url_for("cliente.perfil"))

        # Verificar nombre duplicado
        existe = Usuario.query.filter(
            Usuario.nombre == nombre,
            Usuario.id != usuario.id
        ).first()

        if existe:
            flash("Ese nombre ya está en uso", "error")
            return redirect(url_for("cliente.perfil"))

        usuario.nombre = nombre

        # Cambiar contraseña SOLO si se escribió algo
        if password:
            usuario.set_password(password)

        db.session.commit()

        # Actualizar sesión
        session["usuario"]["nombre"] = usuario.nombre

        flash("Perfil actualizado correctamente", "success")
        return redirect(url_for("cliente.perfil"))

    return render_template("cliente/perfil.html", usuario=usuario)

