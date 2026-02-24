from .database import Base, engine, SessionLocal

# 🔹 EMPRESAS
from .empresa import Empresa

# 🔹 USUARIOS Y SEGURIDAD
from .usuario import (
    Usuario,
    Rol,
    Permiso,
    UsuarioRol,
    RolPermiso
)


# 🔹 PLANES Y PAGOS
from .plan import (
    Plan,
    Suscripcion,
    Pago,
    FacturaSaaS
)


# 🔹 MÓDULOS
from .modulo import (
    Modulo,
    EmpresaModulo
)


# 🔹 CONFIGURACIÓN
from .configuracionEmpresa import (
    ConfiguracionEmpresa,
    PreferenciaUsuario
)


# 🔹 AUDITORÍA
from .auditoria import (
    LogActividad,
    Notificacion,
    HistorialCambios
)


# 🔹 CRM
from .crm import (
    Cliente,
    Contacto,
    SegmentoCliente,
    Interaccion,
    TareaCRM,
    Pipeline,
    EtapaPipeline,
    Oportunidad,
    Actividad
)


# 🔹 VENTAS
from .ventas import (
    Venta,
    DetalleVenta,
    Cotizacion,
    DetalleCotizacion,
    MetodoPago,
    PagoVenta,
    Devolucion,
    NotaCredito
)


# 🔹 COMPRAS
from .compras import (
    Proveedor,
    OrdenCompra,
    DetalleOrdenCompra,
    FacturaProveedor,
    PagoProveedor
)


# 🔹 INVENTARIO
from .inventario import (
    Producto,
    CategoriaProducto,
    VarianteProducto,
    AtributoProducto,
    ImagenProducto,
    Almacen,
    Ubicacion,
    MovimientoStock,
    AjusteStock,
    Lote,
    Serie
)


# 🔹 FINANZAS
from .finanzas import (
    CuentaContable,
    Transaccion,
    LibroDiario,
    Asiento,
    Impuesto,
    CentroCosto,
    FlujoCaja,
    Presupuesto
)


# 🔹 TURNOS Y CALENDARIO
from .turnos import (
    Calendario,
    Evento,
    Turno,
    Recurso,
    Disponibilidad
)


# 🔹 DOCUMENTOS
from .documentos import (
    Archivo,
    Carpeta,
    Documento,
    FirmaDigital
)


# 🔹 WEB Y ECOMMERCE
from .web import (
    PaginaWeb,
    Seccion,
    Bloque,
    Plantilla,
    Dominio,
    SEO,
    Blog,
    EntradaBlog,
    Carrito,
    Pedido,
    DetallePedido,
    Envio,
    MetodoEnvio,
    Direccion
)


# 🔹 RECURSOS HUMANOS
from .empleado import (
    Empleado,
    Asistencia,
    Vacaciones,
    Nomina,
    Contrato,
    Evaluacion
)


# 🔹 ANALÍTICAS
from .analiticas import (
    Reporte,
    Metrica,
    Dashboard,
    Widget
)


# 🔹 IA Y AUTOMATIZACIÓN
from .ia import (
    ReglaAutomatizacion,
    Trigger,
    Accion,
    SugerenciaIA,
    Prediccion
)


# 🔹 INTEGRACIONES
from .integraciones import (
    Integracion,
    APIKey,
    Webhook,
    EventoIntegracion
)


# 🔹 MARKETING
from .marketing import (
    Campana,
    EmailMarketing,
    Segmento,
    Lead,
    Formulario,
    Landing
)


# 🔹 VENTAJAS COMPETITIVAS
from .extras import (
    Workflow,
    Aprobacion,
    NotasInternas,
    Comentarios,
    ChatInterno,
    Encuesta,
    FeedbackCliente
)


# 🔥 FUNCIÓN PARA CREAR TODA LA BASE DE DATOS
def init_db():
    Base.metadata.create_all(engine)