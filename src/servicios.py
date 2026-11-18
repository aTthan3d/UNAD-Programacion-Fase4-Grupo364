"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE SERVICIOS ESPECIALIZADOS (POLIMORFISMO)
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 3 - Entidades de Dominio): [Nombre Compañero 3 / Malkon Alvarez]
Rama de Trabajo: feature/domain-entities-models
========================================================================================
Propósito:
Define la clase abstracta 'Servicio' y 3 subclases especializadas:
1. ReservaSala: Cobro por horas, validación de capacidad de aforo y servicio de refrigerio.
2. AlquilerEquipo: Cobro por días, validación de inventario/stock y depósito de garantía.
3. AsesoriaEspecializada: Cobro por hora profesional, nivel de consultor (Junior, Senior, Master).
Aplica polimorfismo en 'calcular_costo_base()', 'validar_disponibilidad()' y sobrecarga de costos.
========================================================================================
"""

from abc import abstractmethod
from src.base import EntidadBase
from src.exceptions import (
    ServicioError,
    ServicioNoDisponibleError,
    CapacidadExcedidaError,
    StockInsuficienteError
)

# ======================================================================================
# CLASE ABSTRACTA: Servicio
# ======================================================================================
class Servicio(EntidadBase):
    """
    Clase abstracta base para el catálogo de servicios de Software FJ.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        super().__init__(id_servicio)
        if tarifa_base <= 0:
            raise ServicioError(f"La tarifa base del servicio debe ser mayor a 0 (recibido: {tarifa_base}).")
        
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool):
        self._disponible = bool(estado)

    # --- MÉTODO ABSTRACTO 1: Cálculo del costo base ---
    @abstractmethod
    def calcular_costo_base(self, unidades: float) -> float:
        """Calcula el costo bruto del servicio según la unidad de medida (horas, días, etc.)."""
        pass

    # --- MÉTODO ABSTRACTO 2: Validación de disponibilidad de recursos ---
    @abstractmethod
    def validar_disponibilidad(self, **kwargs) -> bool:
        """Verifica que el servicio cumpla las restricciones operativas."""
        pass

    # --- MÉTODO SOBRECARGADO: Cálculo de costo final con impuestos y descuentos ---
    def calcular_costo_total(self, unidades: float, porcentaje_descuento: float = 0.0, porcentaje_iva: float = 19.0) -> float:
        """
        Demuestra sobrecarga de métodos mediante parámetros opcionales.
        Permite calcular el costo neto aplicando opcionalmente descuentos e IVA.
        """
        if unidades <= 0:
            raise ServicioError("Las unidades de servicio solicitadas deben ser mayores a cero.")
        
        costo_base = self.calcular_costo_base(unidades)
        
        # Validación de descuento coherente
        if porcentaje_descuento < 0 or porcentaje_descuento > 100:
            raise ServicioError(f"El porcentaje de descuento ({porcentaje_descuento}%) debe estar entre 0 y 100.")
        
        monto_descuento = costo_base * (porcentaje_descuento / 100.0)
        subtotal = costo_base - monto_descuento
        monto_iva = subtotal * (porcentaje_iva / 100.0)
        costo_final = subtotal + monto_iva
        return round(costo_final, 2)


# ======================================================================================
# SUBCLASE 1: ReservaSala (Reserva de salas de juntas / auditorios)
# ======================================================================================
class ReservaSala(Servicio):
    """
    Servicio de reserva de salas de reuniones.
    Unidad: Horas. Restricción: Aforo máximo de personas.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_por_hora: float, capacidad_maxima: int, tiene_refrigerio: bool = False, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_por_hora, disponible)
        if capacidad_maxima <= 0:
            raise ServicioError("La capacidad máxima de la sala debe ser un entero positivo.")
        self.capacidad_maxima = int(capacidad_maxima)
        self.tiene_refrigerio = tiene_refrigerio
        self.costo_refrigerio_por_persona = 15000.0 if tiene_refrigerio else 0.0

    def validar_disponibilidad(self, **kwargs) -> bool:
        """Valida que la sala esté habilitada y que el número de asistentes no sobrepase el aforo."""
        if not self.disponible:
            raise ServicioNoDisponibleError(self.id_entidad, "La sala se encuentra actualmente en remodelación o mantenimiento.")
        
        asistentes = kwargs.get("asistentes", 1)
        if asistentes > self.capacidad_maxima:
            raise CapacidadExcedidaError(self.capacidad_maxima, asistentes)
        return True

    def calcular_costo_base(self, unidades: float) -> float:
        """Costo = (Horas * Tarifa Hora)"""
        return float(unidades) * self.tarifa_base

    def obtener_resumen(self) -> str:
        ref_txt = "Con Refrigerio" if self.tiene_refrigerio else "Sin Refrigerio"
        return f"Sala [{self.id_entidad}] '{self.nombre}' | Capacidad: {self.capacidad_maxima} pers | ${self.tarifa_base:,.2f}/hr | {ref_txt}"


# ======================================================================================
# SUBCLASE 2: AlquilerEquipo (Equipos de cómputo y audiovisuales)
# ======================================================================================
class AlquilerEquipo(Servicio):
    """
    Servicio de alquiler de laptops de alto rendimiento, proyectores y servidores.
    Unidad: Días. Restricción: Stock disponible en bodega y depósito de garantía.
    """
    def __init__(self, id_servicio: str, nombre: str, tarifa_por_dia: float, stock_disponible: int, deposito_garantia: float = 200000.0, disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_por_dia, disponible)
        if stock_disponible < 0:
            raise ServicioError("El stock disponible no puede ser negativo.")
        self.stock_disponible = int(stock_disponible)
        self.deposito_garantia = float(deposito_garantia)

    def validar_disponibilidad(self, **kwargs) -> bool:
        """Valida que el servicio esté activo y que haya stock suficiente para la cantidad solicitada."""
        if not self.disponible:
            raise ServicioNoDisponibleError(self.id_entidad, "Equipos deshabilitados para calibración técnica.")
        
        cantidad = kwargs.get("cantidad", 1)
        if cantidad > self.stock_disponible:
            raise StockInsuficienteError(self.stock_disponible, cantidad)
        return True

    def calcular_costo_base(self, unidades: float) -> float:
        """Costo = (Días * Tarifa Día) + Depósito de Garantía reembolsable"""
        return (float(unidades) * self.tarifa_base) + self.deposito_garantia

    def obtener_resumen(self) -> str:
        return f"Equipos [{self.id_entidad}] '{self.nombre}' | Stock: {self.stock_disponible} uds | ${self.tarifa_base:,.2f}/día | Depósito: ${self.deposito_garantia:,.2f}"


# ======================================================================================
# SUBCLASE 3: AsesoriaEspecializada (Consultoría técnica y arquitectura de software)
# ======================================================================================
class AsesoriaEspecializada(Servicio):
    """
    Servicio de consultoría tecnológica con especialistas certificados.
    Unidad: Horas. Restricción: Nivel de seniority del asesor (JUNIOR: x1.0, SENIOR: x1.5, MASTER: x2.0).
    """
    MULTIPLICADORES = {
        "JUNIOR": 1.0,
        "SENIOR": 1.5,
        "MASTER": 2.0
    }

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora_base: float, nivel_consultor: str = "SENIOR", disponible: bool = True):
        super().__init__(id_servicio, nombre, tarifa_hora_base, disponible)
        nivel = nivel_consultor.strip().upper()
        if nivel not in self.MULTIPLICADORES:
            raise ServicioError(f"Nivel de consultor inválido ('{nivel_consultor}'). Válidos: JUNIOR, SENIOR, MASTER.")
        self.nivel_consultor = nivel

    def validar_disponibilidad(self, **kwargs) -> bool:
        """Valida que el consultor esté activo en la agenda de la compañía."""
        if not self.disponible:
            raise ServicioNoDisponibleError(self.id_entidad, "El consultor asignado se encuentra en licencia o conferencia.")
        return True

    def calcular_costo_base(self, unidades: float) -> float:
        """Costo = Horas * Tarifa Base * Factor de Seniority"""
        factor = self.MULTIPLICADORES[self.nivel_consultor]
        return float(unidades) * self.tarifa_base * factor

    def obtener_resumen(self) -> str:
        factor = self.MULTIPLICADORES[self.nivel_consultor]
        return f"Asesoría [{self.id_entidad}] '{self.nombre}' | Nivel: {self.nivel_consultor} (x{factor}) | Tarifa Base: ${self.tarifa_base:,.2f}/hr"
