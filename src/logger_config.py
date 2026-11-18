"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE LOGGING
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 1 - Líder de Arquitectura): Malkon Adenir Alvarez Muñoz
Rama de Trabajo: feature/core-logging-base
========================================================================================
Propósito:
Configura y centraliza el sistema de registro de eventos (logging) en archivo plano (software_fj.log)
y en consola. Cumple con el criterio de evaluación de registrar todos los eventos críticos,
operaciones exitosas, advertencias y excepciones del sistema de forma profesional.
========================================================================================
"""

import logging
import os
import sys

# Definición del nombre del archivo donde se guardarán los logs del sistema
LOG_FILE_NAME = "software_fj.log"

def setup_logger(name: str = "SoftwareFJ") -> logging.Logger:
    """
    Configura y retorna una instancia del logger con doble salida:
    1. Archivo persistente 'software_fj.log' con codificación UTF-8 y detalle completo.
    2. Consola estándar para seguimiento en tiempo real durante las simulaciones.
    """
    # Obtiene o crea el logger con el nombre especificado
    logger = logging.getLogger(name)
    
    # Si el logger ya tiene manejadores configurados, lo retorna para evitar mensajes duplicados
    if logger.handlers:
        return logger

    # Establece el nivel mínimo de captura (DEBUG captura todos los eventos informativos y errores)
    logger.setLevel(logging.DEBUG)

    # Formato profesional para cada línea del log: Fecha/Hora - Nivel - Módulo - Mensaje
    log_format = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] (%(name)s:%(module)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 1. Manejador para el archivo de logs (software_fj.log)
    file_handler = logging.FileHandler(LOG_FILE_NAME, mode="a", encoding="utf-8")
    # Registra eventos desde nivel INFO hacia arriba en el archivo persistente
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    # 2. Manejador para la consola estándar (StreamHandler)
    console_handler = logging.StreamHandler(sys.stdout)
    # En consola se muestran advertencias y errores para no saturar la pantalla
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger

# Instancia global del logger lista para ser importada por los demás módulos
logger = setup_logger()
