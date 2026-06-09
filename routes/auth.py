from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session
)

auth_bp = Blueprint(
    "auth",
    __name__
)

ADMIN_USER = "admin"

ADMIN_PASSWORD = "admin123"

# ======================================
# LOGIN
# ======================================

@auth_bp.route(
    "/panel-privado",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        usuario = request.form[
            "usuario"
        ]

        password = request.form[
            "password"
        ]

        if (

            usuario == ADMIN_USER and
            password == ADMIN_PASSWORD

        ):

            session["admin"] = True

            return redirect("/admin")

    return render_template(
        "login.html"
    )

# ======================================
# LOGOUT
# ======================================

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/")