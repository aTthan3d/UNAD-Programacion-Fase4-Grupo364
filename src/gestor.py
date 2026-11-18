"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO GESTOR Y CONTROLADOR DE NEGOCIO
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 4 - Lógica de Negocio y Transacciones): [Nombre Compañero 4 / Malkon Alvarez]
Rama de Trabajo: feature/business-logic-reservations
========================================================================================
Propósito:
Implementa la clase controladora 'GestorSoftwareFJ' que administra las listas en memoria
de clientes, servicios y reservas. Demuestra el uso integral de bloques:
- try / except (captura de errores específicos)
- try / except / else (código que solo se ejecuta en ausencia de fallos)
- try / except / finally (código de limpieza o auditoría obligatoria)
- Encadenamiento de excepciones con 'raise TransaccionError(...) from e'.
========================================================================================
"""

from typing import List, Optional
from src.logger_config import logger
from src.cliente import Cliente
from src.servicios import Servicio
from src.reserva import Reserva, EstadoReserva
from src.exceptions import (
    SoftwareFJError,
    ClienteDuplicadoError,
    ClienteNoEncontradoError,
    ServicioError,
    ReservaError,
    TransaccionError
)

class GestorSoftwareFJ:
    """
    Controlador central del sistema Software FJ.
    Mantiene colecciones internas de datos en memoria sin requerir bases de datos.
    """

    def __init__(self):
        # Listas internas para almacenamiento en memoria
        self.clientes: List[Cliente] = []
        self.servicios: List[Servicio] = []
        self.reservas: List[Reserva] = []
        logger.info("Instancia de GestorSoftwareFJ inicializada con éxito.")

    # ----------------------------------------------------------------------------------
    # GESTIÓN DE CLIENTES CON TRY / EXCEPT / ELSE / FINALLY
    # ----------------------------------------------------------------------------------
    def registrar_cliente(self, id_cliente: str, documento: str, nombre: str, correo: str, telefono: str) -> Optional[Cliente]:
        """
        Registra un nuevo cliente validando unicidad de documento.
        Demuestra bloques try / except / else / finally y encadenamiento de excepciones.
        """
        operacion_exitosa = False
        cliente_creado = None

        try:
            logger.info(f"Iniciando registro de cliente: Documento={documento}, Nombre='{nombre}'...")
            
            # Validación de duplicidad en la lista interna
            for c in self.clientes:
                if c.documento == documento.strip():
                    raise ClienteDuplicadoError(documento)

            # Instanciación (valida internamente los datos con ClienteInvalidoError)
            cliente_creado = Cliente(id_cliente, documento, nombre, correo, telefono)
            self.clientes.append(cliente_creado)

        except SoftwareFJError as err_dominio:
            # Captura de errores propios de negocio
            logger.error(f"Error de dominio al registrar cliente [{documento}]: {err_dominio}")
            # Encadenamiento de excepciones: se reempaqueta con TransaccionError preservando el origen
            raise TransaccionError("Registro de Cliente", str(err_dominio)) from err_dominio

        except Exception as err_inesperado:
            # Captura defensiva de fallos de sistema imprevistos
            logger.critical(f"Fallo crítico no controlado en registro de cliente: {err_inesperado}", exc_info=True)
            raise TransaccionError("Registro de Cliente", "Fallo interno imprevisto") from err_inesperado

        else:
            # BLOQUE ELSE: Se ejecuta ÚNICAMENTE si no ocurrió ninguna excepción en el try
            operacion_exitosa = True
            logger.info(f"Cliente registrado exitosamente en memoria: {cliente_creado.obtener_resumen()}")
            return cliente_creado

        finally:
            # BLOQUE FINALLY: Se ejecuta SIEMPRE para auditoría obligatoria
            estado_txt = "EXITOSA" if operacion_exitosa else "FALLIDA/RECHAZADA"
            logger.debug(f"[AUDITORÍA FINALLY] Fin de transacción de registro cliente ({documento}) -> Estado: {estado_txt}")

    # ----------------------------------------------------------------------------------
    # GESTIÓN DE SERVICIOS
    # ----------------------------------------------------------------------------------
    def registrar_servicio(self, servicio: Servicio):
        """Agrega un servicio al catálogo de la empresa."""
        try:
            if not isinstance(servicio, Servicio):
                raise ServicioError("El objeto a registrar debe heredar de la clase base 'Servicio'.")
            self.servicios.append(servicio)
            logger.info(f"Servicio agregado al catálogo: {servicio.obtener_resumen()}")
        except ServicioError as ex:
            logger.error(f"Rechazado registro de servicio: {ex}")
            raise TransaccionError("Registro de Servicio", str(ex)) from ex

    def buscar_cliente(self, criterio: str) -> Cliente:
        """Busca un cliente por ID o por documento."""
        for c in self.clientes:
            if c.id_entidad == criterio.upper() or c.documento == criterio:
                return c
        raise ClienteNoEncontradoError(criterio)

    def buscar_servicio(self, id_servicio: str) -> Servicio:
        """Busca un servicio en el catálogo por su identificador."""
        for s in self.servicios:
            if s.id_entidad == id_servicio.upper():
                return s
        raise ServicioError(f"Servicio con código '{id_servicio}' no encontrado en el catálogo.")

    # ----------------------------------------------------------------------------------
    # GESTIÓN DE RESERVAS CON ENCADENAMIENTO Y CIERRE DEFENSIVO
    # ----------------------------------------------------------------------------------
    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: float, **parametros_servicio) -> Optional[Reserva]:
        """
        Crea una reserva orquestando cliente y servicio con validación de disponibilidad.
        Demuestra encadenamiento de excepciones ante fallos de aforo, stock o parámetros.
        """
        transaccion_ok = False
        reserva_creada = None

        try:
            logger.info(f"Solicitud de reserva [{id_reserva}]: Cliente={id_cliente}, Servicio={id_servicio}, Duración={duracion}")
            
            # Recupera entidades participantes
            cliente_obj = self.buscar_cliente(id_cliente)
            servicio_obj = self.buscar_servicio(id_servicio)

            # Crea la reserva (valida disponibilidad internamente)
            reserva_creada = Reserva(id_reserva, cliente_obj, servicio_obj, duracion, **parametros_servicio)
            self.reservas.append(reserva_creada)

        except (SoftwareFJError, ValueError) as ex:
            logger.warning(f"Reserva [{id_reserva}] RECHAZADA por regla de negocio: {ex}")
            # ENCADENAMIENTO DE EXCEPCIONES: Mantiene viva la causa original 'ex'
            raise TransaccionError("Creación de Reserva", str(ex)) from ex

        else:
            transaccion_ok = True
            logger.info(f"Reserva creada en estado PENDIENTE: {reserva_creada.obtener_resumen()}")
            return reserva_creada

        finally:
            resultado = "REGISTRADA" if transaccion_ok else "ABORTADA"
            logger.debug(f"[AUDITORÍA FINALLY] Proceso de reserva [{id_reserva}] finalizado. Resultado: {resultado}")

    def procesar_confirmacion(self, id_reserva: str, descuento: float = 0.0) -> float:
        """Confirma una reserva y retorna el monto facturado."""
        reserva = next((r for r in self.reservas if r.id_entidad == id_reserva.upper()), None)
        if not reserva:
            raise ReservaError(f"No existe la reserva [{id_reserva}] para procesar.")
        
        try:
            total = reserva.confirmar(descuento_corporativo=descuento)
            logger.info(f"Reserva [{id_reserva}] CONFIRMADA exitosamente por ${total:,.2f} COP.")
            return total
        except SoftwareFJError as ex:
            logger.error(f"Fallo al confirmar reserva [{id_reserva}]: {ex}")
            raise TransaccionError("Confirmación de Reserva", str(ex)) from ex

    def calcular_total_facturado(self) -> float:
        """Calcula el consolidado financiero de todas las reservas confirmadas o completadas."""
        return sum(r.costo_total for r in self.reservas if r.estado in (EstadoReserva.CONFIRMADA, EstadoReserva.COMPLETADA))
