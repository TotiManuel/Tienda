from functools import wraps
from flask import session, redirect, url_for, abort

def login_requerido(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return wrapper


def rol_requerido(*roles):
    def decorador(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "usuario" not in session:
                return redirect(url_for("auth.login"))

            if session["usuario"]["rol"] not in roles:
                abort(403)

            return f(*args, **kwargs)
        return wrapper
    return decorador
