from functools import wraps
from flask import session, abort
from models.usuario import Usuario


def permiso_requerido(nombre_permiso):

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if "usuario_id" not in session:
                abort(403)

            usuario = Usuario.query.get(session["usuario_id"])

            if not usuario:
                abort(403)

            if not usuario.tiene_permiso(nombre_permiso):
                abort(403)

            return f(*args, **kwargs)

        return wrapper

    return decorator