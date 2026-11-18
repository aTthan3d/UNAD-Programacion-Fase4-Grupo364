"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE RESERVAS
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 4 - Lógica de Negocio y Transacciones): [Nombre Compañero 4 / Malkon Alvarez]
Rama de Trabajo: feature/business-logic-reservations
========================================================================================
Propósito:
Implementa la clase 'Reserva' que articula un Cliente, un Servicio, la duración y su estado.
Gestiona el ciclo de vida de la transacción mediante métodos de confirmación, cancelación y
procesamiento, aplicando validaciones defensivas y excepciones personalizadas.
========================================================================================
"""

from enum import Enum
from src.base import EntidadBase
from src.cliente import Cliente
from src.servicios import Servicio
from src.exceptions import (
    ReservaInvalidaError,
    EstadoReservaInvalidoError
)

class EstadoReserva(Enum):
    """Enumeración con los estados válidos del ciclo de vida de una reserva."""
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"
    COMPLETADA = "COMPLETADA"

class Reserva(EntidadBase):
    """
    Entidad que vincula a un cliente con un servicio solicitado por una duración determinada.
    """
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: float, **parametros_servicio):
        super().__init__(id_reserva)
        
        # Validación de que las entidades asociadas sean instancias válidas
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio válido.")
        if duracion <= 0:
            raise ReservaInvalidaError(f"La duración de la reserva debe ser mayor a cero (recibido: {duracion}).")

        self.cliente = cliente
        self.servicio = servicio
        self.duracion = float(duracion)
        self.parametros_servicio = parametros_servicio
        self._estado = EstadoReserva.PENDIENTE
        self._costo_total = 0.0

        # Al instanciar, verifica de inmediato la disponibilidad del servicio
        self.servicio.validar_disponibilidad(**self.parametros_servicio)
        
        # Calcula el costo base preliminar
        self._costo_total = self.servicio.calcular_costo_total(self.duracion)

    @property
    def estado(self) -> EstadoReserva:
        return self._estado

    @property
    def costo_total(self) -> float:
        return self._costo_total

    def confirmar(self, descuento_corporativo: float = 0.0) -> float:
        """
        Confirma la reserva aplicando un posible descuento corporativo.
        Lanza EstadoReservaInvalidoError si ya no está en estado PENDIENTE.
        """
        if self._estado != EstadoReserva.PENDIENTE:
            raise EstadoReservaInvalidoError(self._estado.value, "Confirmar Reserva")
        
        # Recalcula el costo final aplicando el descuento
        self._costo_total = self.servicio.calcular_costo_total(
            unidades=self.duracion,
            porcentaje_descuento=descuento_corporativo,
            porcentaje_iva=19.0
        )
        self._estado = EstadoReserva.CONFIRMADA
        return self._costo_total

    def cancelar(self, motivo: str = "Solicitud de cliente"):
        """
        Cancela una reserva existente.
        Lanza EstadoReservaInvalidoError si la reserva ya estaba CANCELADA o COMPLETADA.
        """
        if self._estado in (EstadoReserva.CANCELADA, EstadoReserva.COMPLETADA):
            raise EstadoReservaInvalidoError(self._estado.value, f"Cancelar Reserva ({motivo})")
        self._estado = EstadoReserva.CANCELADA

    def completar(self):
        """Marca la reserva como ejecutada y cerrada con éxito."""
        if self._estado != EstadoReserva.CONFIRMADA:
            raise EstadoReservaInvalidoError(self._estado.value, "Completar Servicio")
        self._estado = EstadoReserva.COMPLETADA

    def obtener_resumen(self) -> str:
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado.value} | "
            f"Cliente: {self.cliente.nombre_completo} ({self.cliente.documento}) | "
            f"Servicio: {self.servicio.nombre} (x{self.duracion}) | Total: ${self._costo_total:,.2f}"
        )
