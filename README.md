## 📌 1. Resumen del Proyecto

Este proyecto consiste en una **API REST** diseñada para el registro, consulta y gestión de incidentes tecnológicos internos.

---

## 🎯 2. Objetivo de la Solución

Desarrollar una API REST que permita gestionar incidentes tecnológicos de forma eficiente, facilitando su registro, consulta y seguimiento.

En esto estaremos aplicando las buenas practicas en el desarrollo del backend.

---

### 🛠️ Stack Tecnológico

El proyecto ha sido desarrollado utilizando tecnologías modernas y estándares de la industria para asegurar su escalabilidad y fácil mantenimiento:

*   **Lenguaje:** Python 3.11 (Se utiliza la imagen ligera `python:3.11-alpine3.19` en Docker para optimizar el peso del contenedor).
*   **Base de Datos:** PostgreSQL (Motor relacional robusto para garantizar la integridad de los incidentes).
*   **Contenerización:** Docker y Docker Compose (Aislamiento de entorno, dependencias controladas y despliegue unificado).

---

### 🌟 Buenas Prácticas Aplicadas

Para garantizar un código limpio, mantenible y escalable, la solución no consiste en un script monolítico, sino que implementa los siguientes patrones y principios de diseño:

1.  **Arquitectura por Capas (Separación de Responsabilidades):**
    El proyecto sigue una estructura modular donde cada capa tiene una única responsabilidad:
    *   `api/routes/`: Define los endpoints HTTP y maneja las peticiones de entrada/salida.
    *   `services/`: Contiene la lógica de negocio pura (aislada de la web y de la base de datos).
    *   `repository/`: Abstrae y centraliza toda la interacción con PostgreSQL (implementación del Patrón Repositorio).
2.  **Validación de Datos (`schemas/`):**
    Se utilizan esquemas fuertemente tipados para validar los *payloads* que ingresan por el método POST y para estructurar las respuestas, previniendo errores de consistencia en la base de datos.
3.  **Gestión Segura de Configuraciones (`core/config.py` y `.env`):**
    Cero credenciales "hardcodeadas". La cadena de conexión y otras configuraciones se inyectan a través de variables de entorno, cumpliendo con la metodología *Twelve-Factor App*.
4.  **Trazabilidad y Control de Errores (`core/exceptions.py` y `core/logger.py`):**
    Implementación de un manejo centralizado de excepciones para devolver respuestas HTTP estandarizadas y un sistema de logs para registrar la actividad de la API.
5.  **Optimización de Infraestructura:**
    Uso de un `Dockerfile` basado en Alpine Linux para reducir el tamaño de la imagen final y un `docker-compose.yml` que orquesta la API con su base de datos.
