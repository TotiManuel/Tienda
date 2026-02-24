from datetime import datetime
from extensions import db


class Empleado(db.Model):
    __tablename__ = "empleados"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=True
    )

    nombre = db.Column(db.String(150), nullable=False)
    apellido = db.Column(db.String(150), nullable=False)

    dni = db.Column(db.String(50))
    cuil = db.Column(db.String(50))

    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))

    direccion = db.Column(db.String(300))

    fecha_ingreso = db.Column(db.Date)
    fecha_baja = db.Column(db.Date)

    puesto = db.Column(db.String(150))
    departamento = db.Column(db.String(150))

    salario_base = db.Column(db.Numeric(12, 2))

    tipo_contrato = db.Column(
        db.String(50)
    )  # permanente, temporal, freelance

    estado = db.Column(
        db.String(50),
        default="activo"
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relaciones
    asistencias = db.relationship("Asistencia", backref="empleado", lazy=True)
    vacaciones = db.relationship("Vacaciones", backref="empleado", lazy=True)
    contratos = db.relationship("Contrato", backref="empleado", lazy=True)
    evaluaciones = db.relationship("Evaluacion", backref="empleado", lazy=True)
    
class Asistencia(db.Model):
    __tablename__ = "asistencias"

    id = db.Column(db.Integer, primary_key=True)

    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey("empleados.id"),
        nullable=False
    )

    fecha = db.Column(db.Date, nullable=False)

    hora_entrada = db.Column(db.DateTime)
    hora_salida = db.Column(db.DateTime)

    horas_trabajadas = db.Column(db.Numeric(5, 2))

    tipo = db.Column(
        db.String(50),
        default="presencial"
    )  # remoto, presencial

    estado = db.Column(
        db.String(50),
        default="presente"
    )

    observaciones = db.Column(db.Text)
    
class Vacaciones(db.Model):
    __tablename__ = "vacaciones"

    id = db.Column(db.Integer, primary_key=True)

    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey("empleados.id"),
        nullable=False
    )

    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    dias = db.Column(db.Integer)

    estado = db.Column(
        db.String(50),
        default="pendiente"
    )  # aprobadas, rechazadas

    motivo = db.Column(db.Text)
    
class Nomina(db.Model):
    __tablename__ = "nominas"

    id = db.Column(db.Integer, primary_key=True)

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    periodo = db.Column(db.String(20))

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    estado = db.Column(
        db.String(50),
        default="borrador"
    )

    detalles = db.relationship("DetalleNomina", backref="nomina", lazy=True)
    
class DetalleNomina(db.Model):
    __tablename__ = "detalle_nomina"

    id = db.Column(db.Integer, primary_key=True)

    nomina_id = db.Column(
        db.Integer,
        db.ForeignKey("nominas.id"),
        nullable=False
    )

    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey("empleados.id"),
        nullable=False
    )

    salario = db.Column(db.Numeric(12, 2))
    bonos = db.Column(db.Numeric(12, 2))
    descuentos = db.Column(db.Numeric(12, 2))

    impuestos = db.Column(db.Numeric(12, 2))

    total = db.Column(db.Numeric(12, 2))
    
class Contrato(db.Model):
    __tablename__ = "contratos"

    id = db.Column(db.Integer, primary_key=True)

    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey("empleados.id"),
        nullable=False
    )

    tipo = db.Column(db.String(100))
    salario = db.Column(db.Numeric(12, 2))

    fecha_inicio = db.Column(db.Date)
    fecha_fin = db.Column(db.Date)

    archivo_id = db.Column(
        db.Integer,
        db.ForeignKey("archivos.id")
    )

    estado = db.Column(
        db.String(50),
        default="activo"
    )
    
class Evaluacion(db.Model):
    __tablename__ = "evaluaciones"

    id = db.Column(db.Integer, primary_key=True)

    empleado_id = db.Column(
        db.Integer,
        db.ForeignKey("empleados.id"),
        nullable=False
    )

    evaluador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id")
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    puntuacion = db.Column(db.Numeric(5, 2))

    comentarios = db.Column(db.Text)

    objetivos = db.Column(db.Text)
    
