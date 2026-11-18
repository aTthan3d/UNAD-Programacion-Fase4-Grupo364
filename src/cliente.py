"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE CLIENTE (ENCAPSULAMIENTO Y VALIDACIONES)
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 3 - Entidades de Dominio): [Nombre Compañero 3 / Malkon Alvarez]
Rama de Trabajo: feature/domain-entities-models
========================================================================================
Propósito:
Implementa la clase 'Cliente' heredando de 'EntidadBase'. Aplica encapsulamiento estricto
mediante atributos privados con guion bajo (_), propiedades (@property, @setter) y validación
exhaustiva de formato de correo electrónico, documento numérico y longitud de nombre.
========================================================================================
"""

import re
from src.base import EntidadBase
from src.exceptions import ClienteInvalidoError

class Cliente(EntidadBase):
    """
    Representa a un cliente corporativo o persona natural en Software FJ.
    Protege sus datos mediante encapsulación y validadores de negocio.
    """

    def __init__(self, id_cliente: str, documento: str, nombre_completo: str, correo: str, telefono: str):
        # Inicializa la entidad base con su identificador de sistema
        super().__init__(id_cliente)
        
        # Atributos privados encapsulados
        self._documento = ""
        self._nombre_completo = ""
        self._correo = ""
        self._telefono = ""

        # Asignación a través de los setters para ejecutar las validaciones defensivas
        self.documento = documento
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono

    # --- PROPIEDAD: Documento ---
    @property
    def documento(self) -> str:
        return self._documento

    @documento.setter
    def documento(self, valor: str):
        if not valor or not isinstance(valor, str) or not valor.strip():
            raise ClienteInvalidoError("El documento de identificación no puede estar vacío.")
        limpio = valor.strip()
        # Validación de que contenga solo dígitos numéricos y longitud mínima de 6 caracteres
        if not limpio.isdigit() or len(limpio) < 6:
            raise ClienteInvalidoError(f"Documento inválido ('{valor}'): debe ser numérico y tener mínimo 6 dígitos.")
        self._documento = limpio

    # --- PROPIEDAD: Nombre Completo ---
    @property
    def nombre_completo(self) -> str:
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre completo debe tener al menos 3 caracteres alfabéticos.")
        self._nombre_completo = valor.strip().title()

    # --- PROPIEDAD: Correo Electrónico ---
    @property
    def correo(self) -> str:
        return self._correo

    @correo.setter
    def correo(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ClienteInvalidoError("El correo electrónico es requerido.")
        limpio = valor.strip().lower()
        # Expresión regular estándar para validación sintáctica de email
        patron_email = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron_email, limpio):
            raise ClienteInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = limpio

    # --- PROPIEDAD: Teléfono ---
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ClienteInvalidoError("El número de teléfono no puede estar vacío.")
        limpio = re.sub(r"[^\d+]", "", valor.strip())
        if len(limpio) < 7:
            raise ClienteInvalidoError(f"Número de teléfono demasiado corto ('{valor}'): mínimo 7 dígitos.")
        self._telefono = limpio

    # --- IMPLEMENTACIÓN POLIMÓRFICA DEL MÉTODO ABSTRACTO ---
    def obtener_resumen(self) -> str:
        """Retorna una cadena formal de presentación del cliente."""
        return f"Cliente [{self.id_entidad}] CC: {self.documento} - {self.nombre_completo} | Contacto: {self.correo} / Tel: {self.telefono}"
