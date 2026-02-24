from datetime import datetime
from extensions import db


class Empresa(db.Model):
    __tablename__ = "empresa"

    # 🔹 Identificación básica
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    nombre_legal = db.Column(db.String(200))
    cuit_rut = db.Column(db.String(50))  # adaptable internacional
    tipo_empresa = db.Column(db.String(50))  # comercio, salud, servicio, etc.
    industria = db.Column(db.String(100))

    # 🔹 Contacto
    email = db.Column(db.String(150))
    telefono = db.Column(db.String(50))
    whatsapp = db.Column(db.String(50))
    sitio_web = db.Column(db.String(200))

    # 🔹 Ubicación
    pais = db.Column(db.String(100))
    provincia = db.Column(db.String(100))
    ciudad = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    codigo_postal = db.Column(db.String(20))

    # 🔹 Configuración regional
    idioma = db.Column(db.String(10), default="es")
    zona_horaria = db.Column(db.String(50))
    moneda = db.Column(db.String(10), default="ARS")

    # 🔹 Branding
    logo = db.Column(db.String(300))
    color_principal = db.Column(db.String(20))
    color_secundario = db.Column(db.String(20))
    favicon = db.Column(db.String(300))

    # 🔹 Suscripción y monetización
    plan_id = db.Column(db.Integer, db.ForeignKey("planes.id"))
    estado_suscripcion = db.Column(db.String(50))  # activa, trial, suspendida
    fecha_inicio = db.Column(db.DateTime)
    fecha_vencimiento = db.Column(db.DateTime)
    periodo_facturacion = db.Column(db.String(20))  # mensual, anual
    trial_activo = db.Column(db.Boolean, default=True)

    # 🔹 Límites del plan
    limite_usuarios = db.Column(db.Integer)
    limite_almacenamiento = db.Column(db.Integer)
    limite_sucursales = db.Column(db.Integer)

    # 🔹 Estado del sistema
    activa = db.Column(db.Boolean, default=True)
    bloqueada = db.Column(db.Boolean, default=False)
    motivo_bloqueo = db.Column(db.String(200))

    # 🔹 Seguridad
    verificacion_email = db.Column(db.Boolean, default=False)
    doble_autenticacion = db.Column(db.Boolean, default=False)
    ultimo_acceso = db.Column(db.DateTime)

    # 🔹 Dominio y subdominio
    subdominio = db.Column(db.String(100), unique=True)
    dominio_personalizado = db.Column(db.String(200))
    ssl_activo = db.Column(db.Boolean, default=True)

    # 🔹 Facturación y pagos
    metodo_pago = db.Column(db.String(50))  # tarjeta, mercado pago, etc.
    id_pago_externo = db.Column(db.String(200))
    ultima_factura = db.Column(db.DateTime)

    # 🔹 Configuración operativa
    multi_sucursal = db.Column(db.Boolean, default=False)
    multi_almacen = db.Column(db.Boolean, default=False)
    multi_moneda = db.Column(db.Boolean, default=False)
    multi_idioma = db.Column(db.Boolean, default=False)

    # 🔹 Integraciones
    api_key = db.Column(db.String(200))
    webhook_url = db.Column(db.String(300))
    integraciones_activas = db.Column(db.Text)

    # 🔹 IA y analítica
    analitica_activa = db.Column(db.Boolean, default=True)
    sugerencias_ia = db.Column(db.Boolean, default=False)
    predicciones = db.Column(db.Boolean, default=False)

    # 🔹 Datos internos SaaS
    origen_registro = db.Column(db.String(100))  # ads, referidos
    referencia = db.Column(db.String(100))
    score_cliente = db.Column(db.Float)
    nivel_riesgo = db.Column(db.String(50))

    # 🔹 Auditoría
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # 🔹 Relaciones
    usuarios = db.relationship("Usuario", backref="empresa", lazy=True)