"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - PUNTO DE ENTRADA PRINCIPAL (MAIN)
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado: Consolidación Grupal / Malkon Adenir Alvarez Muñoz
========================================================================================
Este archivo orquesta la ejecución del sistema de gestión de clientes, servicios y
reservas de la empresa 'Software FJ', disparando la batería de 10 simulaciones y
verificando la integridad del registro persistente de logs.
========================================================================================
"""

import os
import sys

# Agrega la raíz del proyecto al path de ejecución para permitir importaciones directas
directorio_raiz = os.path.dirname(os.path.abspath(__file__))
if directorio_raiz not in sys.path:
    sys.path.insert(0, directorio_raiz)

from src.logger_config import logger
from src.simulaciones import ejecutar_bateria_simulaciones

def main():
    """
    Función de arranque del aplicativo.
    """
    logger.info(">>> INICIANDO EJECUCIÓN DEL SISTEMA INTEGRAL SOFTWARE FJ (FASE 4 UNAD) <<<")
    try:
        # Llama a la suite de simulaciones completas
        ejecutar_bateria_simulaciones()
        logger.info(">>> EJECUCIÓN DE SIMULACIONES FINALIZADA CON ÉXITO <<<")
    except Exception as ex_inesperada:
        logger.critical(f"Excepción de nivel superior no controlada: {ex_inesperada}", exc_info=True)
        print(f"\n[ALERTA CRÍTICA]: {ex_inesperada}")

if __name__ == "__main__":
    main()
