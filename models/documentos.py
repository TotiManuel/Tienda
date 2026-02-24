from datetime import datetime
from api.index import db


# 🔹 CARPETA
class Carpeta(db.Model):
    __tablename__ = "carpetas"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)

    carpeta_padre_id = db.Column(
        db.Integer,
        db.ForeignKey("carpetas.id"),
        nullable=True
    )

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)

    # Relaciones
    subcarpetas = db.relationship("Carpeta")
    archivos = db.relationship("Archivo", backref="carpeta", lazy=True)
    
# 🔹 ARCHIVO
class Archivo(db.Model):
    __tablename__ = "archivos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(50))
    tamaño = db.Column(db.Integer)

    ruta = db.Column(db.String(500), nullable=False)

    version = db.Column(db.Integer, default=1)

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    carpeta_id = db.Column(
        db.Integer,
        db.ForeignKey("carpetas.id"),
        nullable=True
    )

    fecha_subida = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    activo = db.Column(db.Boolean, default=True)
    
# 🔹 DOCUMENTO
class Documento(db.Model):
    __tablename__ = "documentos"

    id = db.Column(db.Integer, primary_key=True)

    titulo = db.Column(db.String(200), nullable=False)
    tipo = db.Column(db.String(100))

    estado = db.Column(
        db.String(50),
        default="borrador"
    )  # borrador, aprobado, firmado, rechazado

    cliente_id = db.Column(
        db.Integer,
        db.ForeignKey("clientes.id"),
        nullable=True
    )

    empresa_id = db.Column(
        db.Integer,
        db.ForeignKey("empresas.id"),
        nullable=False
    )

    creador_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    fecha_creacion = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relaciones
    versiones = db.relationship(
        "DocumentoVersion",
        backref="documento",
        lazy=True,
        cascade="all, delete"
    )

    firmas = db.relationship(
        "FirmaDigital",
        backref="documento",
        lazy=True
    )
    
# 🔹 VERSIONES DE DOCUMENTOS (muy importante)
class DocumentoVersion(db.Model):
    __tablename__ = "documento_versiones"

    id = db.Column(db.Integer, primary_key=True)

    documento_id = db.Column(
        db.Integer,
        db.ForeignKey("documentos.id"),
        nullable=False
    )

    archivo_id = db.Column(
        db.Integer,
        db.ForeignKey("archivos.id"),
        nullable=False
    )

    numero_version = db.Column(db.Integer, default=1)

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )
    
# 🔹 FIRMA DIGITAL
class FirmaDigital(db.Model):
    __tablename__ = "firmas_digitales"

    id = db.Column(db.Integer, primary_key=True)

    documento_id = db.Column(
        db.Integer,
        db.ForeignKey("documentos.id"),
        nullable=False
    )

    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("usuarios.id"),
        nullable=False
    )

    fecha = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    hash_documento = db.Column(db.String(255))
    certificado = db.Column(db.Text)

    tipo_firma = db.Column(
        db.String(50),
        default="simple"
    )  # simple, avanzada, biometrica

    valido = db.Column(db.Boolean, default=True)
    
def subir_archivo(file, usuario, empresa, carpeta=None):
    nombre = file.filename
    ruta = f"uploads/{empresa.id}/{nombre}"

    file.save(ruta)

    archivo = Archivo(
        nombre=nombre,
        tipo=file.content_type,
        tamaño=len(file.read()),
        ruta=ruta,
        usuario_id=usuario.id,
        empresa_id=empresa.id,
        carpeta_id=carpeta.id if carpeta else None
    )

    db.session.add(archivo)
    db.session.commit()

    return archivo

def crear_documento(titulo, usuario, empresa, archivo):
    documento = Documento(
        titulo=titulo,
        empresa_id=empresa.id,
        creador_id=usuario.id
    )

    db.session.add(documento)
    db.session.flush()

    version = DocumentoVersion(
        documento_id=documento.id,
        archivo_id=archivo.id,
        numero_version=1,
        usuario_id=usuario.id
    )

    db.session.add(version)
    db.session.commit()

    return documento

import hashlib


def firmar_documento(documento, usuario):
    texto = f"{documento.id}-{usuario.id}-{datetime.utcnow()}"
    hash_doc = hashlib.sha256(texto.encode()).hexdigest()

    firma = FirmaDigital(
        documento_id=documento.id,
        usuario_id=usuario.id,
        hash_documento=hash_doc
    )

    documento.estado = "firmado"

    db.session.add(firma)
    db.session.commit()

    return firma

