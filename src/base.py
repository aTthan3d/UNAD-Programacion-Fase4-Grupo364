"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE CLASE ABSTRACTA BASE
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 1 - Líder de Arquitectura): Malkon Adenir Alvarez Muñoz
Rama de Trabajo: feature/core-logging-base
========================================================================================
Propósito:
Define la clase abstracta 'EntidadBase' que establece la identidad única, auditoría
de creación y contrato común para todas las entidades del dominio (Clientes, Servicios, Reservas).
========================================================================================
"""

from abc import ABC, abstractmethod
from datetime import datetime

class EntidadBase(ABC):
    """
    Clase abstracta base para todas las entidades del sistema Software FJ.
    Garantiza que toda entidad posea un identificador único (id_entidad),
    una marca de tiempo de registro (fecha_registro) y obligue a implementar
    un método polimórfico de representación resumida (obtener_resumen).
    """

    def __init__(self, id_entidad: str):
        # Validación defensiva del identificador
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ValueError("El identificador de la entidad no puede ser nulo o vacío.")
        
        # Identificador inmutable protegido
        self._id_entidad = id_entidad.strip().upper()
        # Marca de tiempo de cuando la entidad fue creada en memoria
        self._fecha_registro = datetime.now()

    @property
    def id_entidad(self) -> str:
        """Getter que permite leer el identificador único de la entidad."""
        return self._id_entidad

    @property
    def fecha_registro(self) -> datetime:
        """Getter que permite consultar la fecha y hora de creación de la entidad."""
        return self._fecha_registro

    @abstractmethod
    def obtener_resumen(self) -> str:
        """
        Método abstracto que cada clase derivada debe sobrescribir obligatoriamente.
        Retorna una cadena descriptiva con el estado y datos principales de la entidad.
        """
        pass

    def __repr__(self) -> str:
        """Representación estándar para depuración."""
        return f"<{self.__class__.__name__} id='{self._id_entidad}'>"
