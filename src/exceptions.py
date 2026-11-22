"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE EXCEPCIONES PERSONALIZADAS
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 2 - Manejo de Errores): [Juan Pablo Santacruz Lopez / Malkon Alvarez]
Rama de Trabajo: feature/custom-exceptions-hierarchy
========================================================================================
Propósito:
Define una jerarquía robusta de excepciones orientadas a objetos que heredan de la clase
base 'SoftwareFJError'. Permite capturar errores de forma granular según la naturaleza
del fallo (validación de clientes, disponibilidad de servicios, inconsistencias de reserva).
========================================================================================
"""

class SoftwareFJError(Exception):
    """
    Clase base para todas las excepciones del dominio Software FJ.
    Permite capturar cualquier error propio del sistema bajo un bloque genérico 'except SoftwareFJError'.
    """
    def __init__(self, mensaje: str, codigo_error: str = "ERR_GENERAL"):
        # Guarda el mensaje descriptivo y un código institucional de auditoría
        self.mensaje = mensaje
        self.codigo_error = codigo_error
        super().__init__(f"[{self.codigo_error}] {self.mensaje}")


# --------------------------------------------------------------------------------------
# 1. EXCEPCIONES ASOCIADAS AL CLIENTE
# --------------------------------------------------------------------------------------

class ClienteError(SoftwareFJError):
    """Excepción base para fallos asociados a la entidad Cliente."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_CLIENTE"):
        super().__init__(mensaje, codigo_error)

class ClienteInvalidoError(ClienteError):
    """Lanzada cuando los datos personales del cliente no superan las reglas de validación."""
    def __init__(self, mensaje: str, campo: str | None = None):
        self.campo = campo
        super().__init__(mensaje, codigo_error="ERR_CLIENTE_DATOS_INVALIDOS")

class ClienteDuplicadoError(ClienteError):
    """Lanzada cuando se intenta registrar un cliente con un documento ya existente."""
    def __init__(self, documento: str):
        self.documento = documento
        super().__init__(f"Ya existe un cliente registrado con el documento '{documento}'.", codigo_error="ERR_CLIENTE_DUPLICADO")

class ClienteNoEncontradoError(ClienteError):
    """Lanzada cuando se busca un cliente inexistente en el sistema."""
    def __init__(self, identificador: str):
        self.identificador = identificador
        super().__init__(f"No se encontró ningún cliente con el ID/Documento '{identificador}'.", codigo_error="ERR_CLIENTE_NO_ENCONTRADO")


# --------------------------------------------------------------------------------------
# 2. EXCEPCIONES ASOCIADAS A LOS SERVICIOS
# --------------------------------------------------------------------------------------

class ServicioError(SoftwareFJError):
    """Excepción base para fallos en la configuración o disponibilidad de servicios."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_SERVICIO"):
        super().__init__(mensaje, codigo_error)

class ServicioNoDisponibleError(ServicioError):
    """Lanzada cuando un servicio está inactivo o fuera de servicio por mantenimiento."""
    def __init__(self, codigo_servicio: str, razon: str = "Servicio inactivo"):
        self.codigo_servicio = codigo_servicio
        self.razon = razon
        super().__init__(f"El servicio '{codigo_servicio}' no está disponible: {razon}.", codigo_error="ERR_SERVICIO_NO_DISPONIBLE")

class CapacidadExcedidaError(ServicioError):
    """Lanzada cuando la cantidad de asistentes supera el aforo de la sala de reuniones."""
    def __init__(self, capacidad_maxima: int, asistentes_solicitados: int):
        self.capacidad_maxima = capacidad_maxima
        self.asistentes_solicitados = asistentes_solicitados
        mensaje = f"Aforo superado: Capacidad máxima={capacidad_maxima}, solicitados={asistentes_solicitados}."
        super().__init__(mensaje, codigo_error="ERR_CAPACIDAD_EXCEDIDA")

class StockInsuficienteError(ServicioError):
    """Lanzada cuando la cantidad de equipos solicitados supera el inventario disponible."""
    def __init__(self, stock_actual: int, cantidad_solicitada: int):
        self.stock_actual = stock_actual
        self.cantidad_solicitada = cantidad_solicitada
        mensaje = f"Inventario insuficiente: Disponibles={stock_actual}, solicitados={cantidad_solicitada}."
        super().__init__(mensaje, codigo_error="ERR_STOCK_INSUFICIENTE")


# --------------------------------------------------------------------------------------
# 3. EXCEPCIONES ASOCIADAS A LAS RESERVAS Y TRANSACCIONES
# --------------------------------------------------------------------------------------

class ReservaError(SoftwareFJError):
    """Excepción base para inconsistencias en el ciclo de vida de una reserva."""
    def __init__(self, mensaje: str, codigo_error: str = "ERR_RESERVA"):
        super().__init__(mensaje, codigo_error)

class ReservaInvalidaError(ReservaError):
    """Lanzada cuando los parámetros de la reserva (duración, fechas, tarifas) son inconsistentes."""
    def __init__(self, mensaje: str):
        super().__init__(mensaje, codigo_error="ERR_RESERVA_PARAMETROS_INVALIDOS")

class EstadoReservaInvalidoError(ReservaError):
    """Lanzada cuando se intenta una transición de estado ilegal (ej. cancelar una reserva ya cancelada)."""
    def __init__(self, estado_actual: str, accion_intentada: str):
        self.estado_actual = estado_actual
        self.accion_intentada = accion_intentada
        mensaje = f"No es posible ejecutar '{accion_intentada}' sobre una reserva en estado '{estado_actual}'."
        super().__init__(mensaje, codigo_error="ERR_ESTADO_RESERVA_ILEGAL")

class TransaccionError(SoftwareFJError):
    """
    Excepción utilizada para ENCADENAMIENTO DE EXCEPCIONES (raise TransaccionError from error_previo).
    Representa una falla global en una operación de negocio debido a causas subyacentes.
    """
    def __init__(self, operacion: str, razon: str):
        self.operacion = operacion
        self.razon = razon
        super().__init__(f"Fallo en la transacción '{operacion}': {razon}", codigo_error="ERR_TRANSACCION_FALLIDA")
