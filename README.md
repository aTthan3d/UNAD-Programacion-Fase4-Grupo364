# Sistema Integral de Gestión de Clientes, Servicios y Reservas — Software FJ
**Curso:** Programación (213023) - Universidad Nacional Abierta y a Distancia (UNAD)  
**Fase 4:** Componente Práctico - Prácticas Simuladas (Manejo Avanzado de Excepciones)  
**Grupo Colaborativo:** 213023_364  

---

## 📌 Descripción del Proyecto
Este proyecto implementa una arquitectura orientada a objetos en **Python 3**, sin uso de motores de base de datos relacionales ni NoSQL. Toda la persistencia opera en estructuras de datos en memoria (listas y objetos), garantizando la estabilidad y robustez del sistema mediante una gestión avanzada de excepciones (`try/except/else/finally`), jerarquía de excepciones personalizadas, encadenamiento de causas (`raise ... from e`) y auditoría persistente mediante el módulo estándar `logging`.

La solución modela la operación integral de **Software FJ**, gestionando clientes corporativos, catálogo de servicios polimórficos (reservas de salas de juntas, alquiler de equipos tecnológicos y asesorías especializadas) y orquestación de reservas con validaciones estrictas de aforo, stock y disponibilidad.

---

## 👥 Distribución de Roles y Ramas de Trabajo (5 Integrantes)

Para cumplir con el cuarto criterio de la rúbrica de evaluación (*Trabajo Colaborativo y Uso Profesional de GitHub*), el desarrollo se dividió en las siguientes ramas de trabajo asignadas a los roles del equipo:

| Integrante / Rol Asignado | Rama de Trabajo | Módulos y Responsabilidades |
| :--- | :--- | :--- |
| **Integrante 1 (Líder / Arquitectura y Logging):**<br>Malkon Adenir Alvarez Muñoz | `feature/core-logging-base` | • Estructura base del repositorio y `README.md`.<br>• Configuración del sistema de `logging` en archivo `software_fj.log`.<br>• Clase abstracta base `EntidadBase` en `src/base.py`. |
| **Integrante 2 (Manejo de Errores y Excepciones):**<br>Juan Pablo Santacruz López | `feature/custom-exceptions-hierarchy` | • Jerarquía de excepciones personalizadas en `src/exceptions.py`.<br>• Definición de `SoftwareFJError`, `ClienteError`, `ServicioError`, `ReservaError` y `TransaccionError`. |
| **Integrante 3 (Entidades de Dominio y Polimorfismo):**<br>Consolidación Equipo | `feature/domain-entities-models` | • Encapsulación y validación de expresiones regulares en `src/cliente.py`.<br>• Clase abstracta `Servicio` y subclases polimórficas (`ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`) en `src/servicios.py`. |
| **Integrante 4 (Lógica de Negocio y Transacciones):**<br>Kevin Andrés Vásquez | `feature/business-logic-reservations` | • Ciclo de vida y estados de `Reserva` en `src/reserva.py`.<br>• Controlador central `GestorSoftwareFJ` en `src/gestor.py` con bloques `try/except/else/finally` y encadenamiento de excepciones. |
| **Integrante 5 (Control de Calidad y Simulaciones):**<br>Consolidación Equipo | `feature/system-simulations-runner` | • Suite de **10 simulaciones completas** en `src/simulaciones.py`.<br>• Punto de entrada principal en `main.py`.<br>• Auditoría de estabilidad y cero interrupciones ante fallos graves. |

---

## 🏗️ Estructura del Repositorio

```text
SoftwareFJ_Payroll_System/
├── README.md                 # Documentación técnica y guía de colaboración
├── .gitignore                # Reglas de exclusión para Python y logs temporales
├── main.py                   # Orquestador y punto de entrada de la aplicación
├── software_fj.log           # Archivo generado con la auditoría en tiempo real de eventos
└── src/
    ├── __init__.py           # Inicializador de paquete Python
    ├── base.py               # Clase abstracta 'EntidadBase'
    ├── logger_config.py      # Configuración del logger estándar dual (consola y archivo)
    ├── exceptions.py         # Jerarquía de excepciones personalizadas
    ├── cliente.py            # Clase Cliente con encapsulamiento estricto
    ├── servicios.py          # Clase abstracta Servicio y 3 clases polimórficas
    ├── reserva.py            # Entidad Reserva y cálculo sobrecargado de costos
    ├── gestor.py             # Controlador de negocio y manejo de transacciones
    └── simulaciones.py       # Batería de 10 simulaciones (5 válidas y 5 inválidas)
```

---

## ⚡ Batería de 10 Simulaciones Ejecutadas

El sistema valida su capacidad de recuperación y estabilidad continua ejecutando:

1. **[Simulación 01 - Éxito]:** Registro de cliente natural con validación de cédula, correo y teléfono.
2. **[Simulación 02 - Éxito]:** Registro de cliente corporativo (Tech Solutions S.A.S).
3. **[Simulación 03 - Éxito]:** Creación y confirmación de reserva de sala de reuniones (8 asistentes / capacidad 12) con descuento corporativo del 10%.
4. **[Simulación 04 - Éxito]:** Alquiler de 3 laptops de desarrollo por 5 días con depósito de garantía.
5. **[Simulación 05 - Éxito]:** Contratación de 10 horas de consultoría cloud nivel Master (factor x2.0).
6. **[Simulación 06 - Error Controlado]:** Rechazo de registro por correo electrónico mal formado sintácticamente (`ClienteInvalidoError`).
7. **[Simulación 07 - Error Controlado]:** Rechazo por intento de duplicación de documento existente (`ClienteDuplicadoError`).
8. **[Simulación 08 - Error Controlado]:** Rechazo de reserva de sala por aforo superado (25 personas en sala para 12) (`CapacidadExcedidaError`).
9. **[Simulación 09 - Error Controlado]:** Rechazo de alquiler de equipos por stock insuficiente en bodega (`StockInsuficienteError`).
10. **[Simulación 10 - Error Controlado]:** Rechazo de reserva en servicio inactivo / en mantenimiento (`ServicioNoDisponibleError`).

**Resultado:** Cero caídas de ejecución. Todas las excepciones fueron capturadas, encadenadas con `TransaccionError` y auditadas en `software_fj.log`.

---

## 🚀 Instrucciones de Ejecución

Para clonar y ejecutar el proyecto localmente:

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO_GITHUB>
cd SoftwareFJ_Payroll_System

# 2. Ejecutar la suite de simulaciones
python main.py

# 3. Inspeccionar el archivo de logs generado
cat software_fj.log
```
