"""
========================================================================================
SISTEMA INTEGRAL SOFTWARE FJ - MÓDULO DE SIMULACIONES Y PRUEBAS DEL SISTEMA
Curso: Programación (Código 213023) - UNAD | Fase 4: Prácticas Simuladas
Rol Asignado (Integrante 5 - Control de Calidad y Simulaciones): [Nombre Compañero 5 / Malkon Alvarez]
Rama de Trabajo: feature/system-simulations-runner
========================================================================================
Propósito:
Ejecuta de manera secuencial y controlada al menos 10 simulaciones completas:
- 5 Operaciones Exitosas (clientes válidos, reservas en sala, alquiler de laptops, consultoría máster).
- 5 Operaciones Inválidas con errores controlados (documento corrupto, correo mal formado,
  aforo de sala superado, stock de laptops agotado, doble confirmación ilegal).
Demuestra que el sistema NUNCA se detiene ante excepciones graves y registra toda la
auditoría en 'software_fj.log'.
========================================================================================
"""

import sys
from src.logger_config import logger
from src.gestor import GestorSoftwareFJ
from src.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from src.exceptions import TransaccionError

def ejecutar_bateria_simulaciones():
    """
    Función principal que coordina las 10 simulaciones requeridas por la guía.
    """
    print("=" * 85)
    print("       EMPRESA 'SOFTWARE FJ' - SUITE DE SIMULACIONES Y MANEJO DE EXCEPCIONES")
    print("       Curso: Programación (213023) - UNAD | Fase 4: Prácticas Simuladas")
    print("=" * 85)
    print(f"[*] Registrando eventos en tiempo real en archivo: software_fj.log\n")

    gestor = GestorSoftwareFJ()

    # Pre-carga del catálogo de servicios
    sala_innovacion = ReservaSala("SRV-SALA-01", "Sala de Innovación y Diseño", tarifa_por_hora=65000.0, capacidad_maxima=12, tiene_refrigerio=True)
    laptops_dev = AlquilerEquipo("SRV-EQP-01", "Laptops Dell Precision (i7/32GB)", tarifa_por_dia=95000.0, stock_disponible=5, deposito_garantia=300000.0)
    asesor_cloud = AsesoriaEspecializada("SRV-ASE-01", "Arquitectura Cloud en AWS/Azure", tarifa_hora_base=120000.0, nivel_consultor="MASTER")
    sala_mantenimiento = ReservaSala("SRV-SALA-02", "Auditorio Central", tarifa_por_hora=150000.0, capacidad_maxima=50, disponible=False)

    for srv in (sala_innovacion, laptops_dev, asesor_cloud, sala_mantenimiento):
        gestor.registrar_servicio(srv)

    print("\n" + "#" * 85)
    print("### BLOQUE 1: SIMULACIONES DE OPERACIONES VÁLIDAS (CASOS DE ÉXITO)")
    print("#" * 85)

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 1: Registro correcto de Cliente 1
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 01]: Registro Exitoso de Cliente Natural...")
    try:
        c1 = gestor.registrar_cliente("CLI-001", "1114885230", "Malkon Alvarez", "malkon.alvarez@unad.edu.co", "3154889900")
        print(f"    [OK] Éxito: {c1.obtener_resumen()}")
    except TransaccionError as ex:
        print(f"    [FALLO INESPERADO]: {ex}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 2: Registro correcto de Cliente Corporativo
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 02]: Registro Exitoso de Cliente Empresarial...")
    try:
        c2 = gestor.registrar_cliente("CLI-002", "901458789", "Tech Solutions S.A.S", "contacto@techsolutions.com", "6022889900")
        print(f"    [OK] Éxito: {c2.obtener_resumen()}")
    except TransaccionError as ex:
        print(f"    [FALLO INESPERADO]: {ex}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 3: Creación y confirmación de Reserva de Sala dentro del aforo
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 03]: Reserva de Sala con 8 asistentes (Capacidad: 12)...")
    try:
        r1 = gestor.crear_reserva("RES-101", "CLI-001", "SRV-SALA-01", duracion=4.0, asistentes=8)
        total = gestor.procesar_confirmacion("RES-101", descuento=10.0)
        print(f"    [OK] Éxito: Reserva confirmada por ${total:,.2f} COP con 10% desc.")
    except TransaccionError as ex:
        print(f"    [FALLO INESPERADO]: {ex}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 4: Alquiler de Equipos dentro del stock disponible
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 04]: Alquiler de 3 Laptops por 5 días (Stock: 5)...")
    try:
        r2 = gestor.crear_reserva("RES-102", "CLI-002", "SRV-EQP-01", duracion=5.0, cantidad=3)
        total = gestor.procesar_confirmacion("RES-102", descuento=5.0)
        print(f"    [OK] Éxito: Alquiler confirmado por ${total:,.2f} COP (incluye depósito).")
    except TransaccionError as ex:
        print(f"    [FALLO INESPERADO]: {ex}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 5: Asesoría Técnica Especializada (Nivel Master)
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 05]: Contratación de Asesoría Cloud Master por 10 horas...")
    try:
        r3 = gestor.crear_reserva("RES-103", "CLI-002", "SRV-ASE-01", duracion=10.0)
        total = gestor.procesar_confirmacion("RES-103", descuento=15.0)
        print(f"    [OK] Éxito: Asesoría confirmada por ${total:,.2f} COP con factor Master.")
    except TransaccionError as ex:
        print(f"    [FALLO INESPERADO]: {ex}")

    print("\n" + "#" * 85)
    print("### BLOQUE 2: SIMULACIONES DE OPERACIONES INVÁLIDAS (CONTROL DE EXCEPCIONES)")
    print("#" * 85)

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 6: Intento de registro con Formato de Correo Inválido
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 06]: Intento de Registro con Email Erróneo (sin '@' o sin dominio)...")
    try:
        gestor.registrar_cliente("CLI-003", "1005889911", "Carlos Pérez", "correo_sin_formato_valido", "3001234567")
    except TransaccionError as ex:
        print(f"    [CONTROLADO]: Transacción rechazada correctamente.")
        print(f"    -> Detalle de Excepción: {ex}")
        print(f"    -> Causa Subyacente (Chained): {type(ex.__cause__).__name__}: {ex.__cause__}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 7: Intento de registro con Documento Duplicado
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 07]: Intento de Registro con Cédula ya existente (1114885230)...")
    try:
        gestor.registrar_cliente("CLI-004", "1114885230", "Homónimo Intruso", "otro@correo.com", "3119998877")
    except TransaccionError as ex:
        print(f"    [CONTROLADO]: Detección de duplicado interceptada con éxito.")
        print(f"    -> Detalle de Excepción: {ex}")
        print(f"    -> Causa Subyacente: {type(ex.__cause__).__name__}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 8: Reserva de Sala superando el Aforo Máximo Permitido
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 08]: Intento de Reserva con 25 personas en Sala para 12...")
    try:
        gestor.crear_reserva("RES-104", "CLI-001", "SRV-SALA-01", duracion=2.0, asistentes=25)
    except TransaccionError as ex:
        print(f"    [CONTROLADO]: Violación de capacidad máxima rechazada sin colapsar el sistema.")
        print(f"    -> Detalle de Excepción: {ex}")
        print(f"    -> Causa Subyacente: {type(ex.__cause__).__name__}: {ex.__cause__}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 9: Alquiler de Equipos solicitando más unidades de las disponibles en bodega
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 09]: Solicitud de 10 Laptops (Stock actual en bodega: 5)...")
    try:
        gestor.crear_reserva("RES-105", "CLI-002", "SRV-EQP-01", duracion=3.0, cantidad=10)
    except TransaccionError as ex:
        print(f"    [CONTROLADO]: Stock insuficiente manejado de forma limpia.")
        print(f"    -> Detalle de Excepción: {ex}")
        print(f"    -> Causa Subyacente: {type(ex.__cause__).__name__}")

    # ----------------------------------------------------------------------------------
    # SIMULACIÓN 10: Reserva en Servicio Inactivo / Fuera de Servicio
    # ----------------------------------------------------------------------------------
    print("\n>>> [SIMULACIÓN 10]: Intento de Reserva en Auditorio Central en Mantenimiento...")
    try:
        gestor.crear_reserva("RES-106", "CLI-001", "SRV-SALA-02", duracion=4.0, asistentes=30)
    except TransaccionError as ex:
        print(f"    [CONTROLADO]: Servicio inactivo rechazado oportunamente.")
        print(f"    -> Detalle de Excepción: {ex}")
        print(f"    -> Causa Subyacente: {type(ex.__cause__).__name__}: {ex.__cause__}")

    # Resumen general del sistema
    print("\n" + "=" * 85)
    print("                    CONSOLIDADO FINAL DE LA SIMULACIÓN")
    print("=" * 85)
    print(f"Total Clientes registrados en memoria: {len(gestor.clientes)}")
    print(f"Total Servicios en catálogo:           {len(gestor.servicios)}")
    print(f"Total Reservas gestionadas:            {len(gestor.reservas)}")
    print(f"Monto Total Facturado con éxito:       ${gestor.calcular_total_facturado():,.2f} COP")
    print("Estado de Estabilidad del Sistema:     100% OPERATIVO (CERO CAÍDAS ANTE ERRORES)")
    print("=" * 85)
