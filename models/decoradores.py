from functools import wraps
from flask import session, redirect, url_for
from models.usuario import Usuario

def permiso_requerido(permiso):

    def decorador(f):
        @wraps(f)
        def funcion(*args, **kwargs):

            if "usuario_id" not in session:
                return redirect(url_for("login"))

            usuario = Usuario.query.get(session["usuario_id"])

            if not usuario or not usuario.tiene_permiso(permiso):
                return "No autorizado", 403

            return f(*args, **kwargs)

        return funcion
    return decorador