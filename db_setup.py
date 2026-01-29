from app import create_app
from models import db, Usuario, Configuracion

def init_db():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # Configuración por defecto
        if not Configuracion.query.first():
            defaults = [
                Configuracion(clave="nombre_tienda", valor="Mi Tienda"),
                Configuracion(clave="email_contacto", valor="contacto@mitienda.com"),
                Configuracion(clave="telefono_contacto", valor="+34 600 123 456"),
                Configuracion(clave="impuesto", valor="21"),
                Configuracion(clave="descuento_maximo", valor="50")
            ]
            db.session.add_all(defaults)

        # Usuarios de ejemplo
        if not Usuario.query.filter_by(nombre="admin").first():
            admin = Usuario(nombre="admin", rol="admin")
            admin.set_password("1234")
            vendedor = Usuario(nombre="vendedor", rol="vendedor")
            vendedor.set_password("1234")
            cliente = Usuario(nombre="cliente", rol="cliente")
            cliente.set_password("1234")
            db.session.add_all([admin, vendedor, cliente])

        db.session.commit()
        print("Base de datos inicializada correctamente.")

if __name__ == "__main__":
    init_db()
