from app.database import db
from datetime import datetime

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    total = db.Column(db.Float, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default="finalizada")

    # 🔥 Nuevo: método de pago
    metodo_pago = db.Column(db.String(50), default="Efectivo")

    detalles = db.relationship(
        "DetalleVenta",
        backref="venta",
        cascade="all, delete",
        lazy=True
    )

    @staticmethod
    def obtener_carrito():
        carrito = Venta.query.filter_by(estado="carrito").first()
        if not carrito:
            carrito = Venta(total=0, estado="carrito")
            db.session.add(carrito)
            db.session.commit()
        return carrito

    def recalcular_total(self):
        self.total = sum(d.subtotal for d in self.detalles)
        db.session.commit()

    def confirmar(self, metodo="Efectivo"):
        self.estado = "finalizada"
        self.fecha = datetime.utcnow()
        self.metodo_pago = metodo
        self.recalcular_total()
        db.session.commit()

    def vaciar(self):
        for d in self.detalles:
            db.session.delete(d)
        self.total = 0
        db.session.commit()
