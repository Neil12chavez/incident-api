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

---

### 🏗️ Arquitectura y Flujo de Desarrollo (Deep Dive)

Para garantizar un código ordenado y escalable, el desarrollo no se realizó en un solo archivo. Se utilizó una **Arquitectura de N Capas**, construyendo el proyecto desde la capa de datos hacia la capa de presentación web. 

![Infraestructura](/image/diagrama_incident.png)

Aqui detallo como realice la creación de cada módulo:

#### 1. Los Cimientos: Configuración y Base de Datos (`core/` y `db/`)
El primer paso fue establecer la conexión con PostgreSQL y definir la estructura de la base de datos.
*   **`core/config.py` y `.env`**: Se crearon para centralizar la lectura de variables de entorno (como `DATABASE_URL`). Esto asegura que las credenciales no estén en el código fuente.
*   **`db/database.py`**: Aquí se configuró el motor de la base de datos y la sesión. Sirve como el puente principal para que la aplicación pueda ejecutar transacciones.
*   **`db/models.py`**: Se definió el modelo de la entidad `Incident` (ORM). Este archivo mapea la clase de Python directamente a la tabla física en PostgreSQL.

#### 2. La Validación: Contratos de Datos (`schemas/`)
Antes de recibir información del usuario, necesitábamos definir qué datos son válidos.
*   **`schemas/incident.py`**: Se crearon los esquemas de validación (generalmente usando librerías como Pydantic/Marshmallow). 
    *   *¿Para qué sirve?* Define un esquema para crear incidentes (exigiendo título, descripción, etc.) y otro para responder (excluyendo datos sensibles y formateando fechas). Se importa en las rutas para validar automáticamente el cuerpo de la petición (Payload).

#### 3. Acceso a Datos: El Patrón Repositorio (`repository/`)
Para no acoplar la lógica de negocio directamente con el ORM de la base de datos, creamos una capa intermedia.
*   **`repository/incident_repository.py`**: Contiene las operaciones CRUD puras (Crear, Leer, Buscar por ID). 
    *   *¿Por qué hacerlo así?* Si en el futuro cambiamos PostgreSQL por MongoDB, solo modificamos este archivo, dejando el resto de la aplicación intacta. Este módulo importa `models.py` y la sesión de `database.py`.

#### 4. La Lógica de Negocio (`services/`)
Aquí es donde reside el "cerebro" de la aplicación.
*   **`services/incident_service.py`**: Intermediario entre la API y el repositorio. 
    *   *Contexto:* Este servicio importa el repositorio. Si un usuario busca el incidente `ID=5` y no existe, el repositorio devuelve un dato vacío, pero el *servicio* es el encargado de lanzar un error "404 Not Found".

#### 5. Exposición Web: Controladores y Rutas (`api/`)
Una vez que el núcleo funcionaba, creamos las puertas de entrada HTTP.
*   **`api/v1/routes/incident.py`**: Aquí se definen los endpoints (`POST /incidents`, `GET /incidents`, `GET /incidents/{id}`).
    *   *Flujo:* Este archivo importa los `schemas` (para validar lo que entra) y el `incident_service` (para procesar la petición). Aquí solo se gestiona la comunicación HTTP (recibir JSON, devolver JSON).
*   **`api/v1/routes/health.py`**: Un endpoint adicional de buenas prácticas (`GET /health`) para que Docker y los balanceadores de carga puedan verificar si la API está viva.

#### 6. El Ensamblaje Final: El Punto de Entrada (`main.py`)
El último archivo en codificarse fue el orquestador principal.
*   **`app/main.py`**: Es el archivo que arranca la aplicación. 
    *   *¿Qué hace?* Importa las rutas de `incident.py` y `health.py` y las registra en el framework web. Además, inicializa el manejo de errores globales (`core/exceptions.py`) y la configuración de registros (`core/logger.py`) para tener observabilidad en la consola de Docker.

---

### 🚀 Guía de Replicación y Despliegue

Sigue estos pasos para levantar el proyecto en tu entorno local. Gracias a la contenerización, el proceso es sumamente sencillo y no requiere instalar Python ni PostgreSQL directamente en tu máquina.

#### 1. Requisitos Previos

Asegúrate de tener instaladas las siguientes herramientas:
* **Docker Desktop**
* **Git**
* Una herramienta para consumir la API (**Postman**, **Insomnia** o la misma terminal usando `curl`).

#### 2. Configuración del Entorno

El proyecto utiliza variables de entorno para manejar las credenciales de manera segura. En la raíz del proyecto, debes contar con un archivo `.env`[cite: 2]. 

#### 3. Ejecución del Entorno

Para levantar toda la solución (el motor de PostgreSQL y la API) de forma orquestada, abre tu terminal en la raíz del proyecto y ejecuta el siguiente comando:

```bash
docker compose up --build
```

#### 4. Verificación del Despliegue

Una vez que la terminal indique que los contenedores están en ejecución, puedes verificar que la aplicación está saludable realizando una petición GET al endpoint de diagnóstico:

```bash
curl http://localhost:8000/api/v1/health
```

---

### 📡 Documentación de la API (Endpoints)

La API expone los siguientes endpoints RESTful para la gestión de incidentes TI, consumiendo y produciendo formato JSON.

#### 1. Registrar un nuevo incidente
*   **Ruta:** `POST /incidents`
*   **Descripción:** Crea un nuevo registro de incidente tecnológico en el sistema.

**Ejemplo de Petición (cURL):**
```bash
curl --location 'http://localhost:8000/api/v1/incidents' \
--header 'Content-Type: application/json' \
--data '{
    "title": "Falla en conexión a VPN",
    "description": "Los usuarios de la sede central no pueden conectarse a la VPN corporativa desde las 08:00 AM.",
    "severity": "Alta",
    "reporter_email": "ejemplo@gmail.com"
}' 
```

**Ejemplo de Respuesta (201 Created):**
```json
{
    "id": 1,
    "title": "Falla en conexión a VPN",
    "description": "Los usuarios de la sede central no pueden conectarse a la VPN corporativa desde las 08:00 AM.",
    "severity": "Alta",
    "reporter_email": "ejemplo@gmail.com",
    "status": "Abierto",
    "created_at": "2026-05-06T10:30:00Z"
}
```


#### 2. Listar todos los incidentes
*   **Ruta:** `GET /incidents`
*   **Descripción:** Retorna una lista con todos los incidentes registrados en la base de datos.

**Ejemplo de Petición (cURL):**
```bash
curl --location 'http://localhost:8000/api/v1/incidents'
```

**Ejemplo de Respuesta (200 OK)**
```json
[
    {
        "id": 1,
        "title": "Falla en conexión a VPN",
        "severity": "Alta",
        "status": "Abierto",
        "created_at": "2026-05-06T10:30:00Z"
    },
    {
        "id": 2,
        "title": "Reinicio inesperado del servidor de base de datos",
        "severity": "Crítica",
        "status": "En Progreso",
        "created_at": "2026-05-05T15:45:00Z"
    }
]
```

#### 3. Consultar un incidente específico por ID
*   **Ruta:** `GET /incidents/{id}`
*   **Descripción:** Obtiene los detalles completos de un incidente específico utilizando su identificador único.

**Ejemplo de Petición (cURL):**
```bash
curl --location 'http://localhost:8000/api/v1/incidents/1'
```

**Ejemplo de Respuesta (200 OK):**
```json
{
    "id": 1,
    "title": "Falla en conexión a VPN",
    "description": "mmmm"
}
```

**Ejemplo de Respuesta de Error (404 Not Found):**
```json
{
    "detail": "Incidente con ID 1 no encontrado."
}
```

### 📂 Estructura Detallada del Repositorio

El proyecto mantiene una estructura de directorios limpia y escalable. A continuación, se detalla la organización de los archivos principales:

```text
.
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── routes/
│   │           ├── health.py               # Endpoint de diagnóstico para Docker
│   │           └── incident.py             # Endpoints HTTP de incidentes
│   ├── core/
│   │   ├── config.py                       # Carga de variables de entorno
│   │   └── exceptions.py                   # Manejo global de errores HTTP
│   ├── db/
│   │   ├── database.py                     # Configuración y conexión con PostgreSQL
│   │   └── models.py                       # Entidades ORM (Tablas de base de datos)
│   ├── repository/
│   │   └── incident_repository.py          # Consultas a base de datos (CRUD)
│   ├── schemas/
│   │   └── incident.py                     # Contratos y validación de datos de entrada/salida
│   ├── services/
│   │   └── incident_service.py             # Lógica de negocio e intermediario API-BD
│   └── main.py                             # Orquestador y punto de entrada de la API
├── .env                                    # Archivo de variables de entorno (no versionado)
├── docker-compose.yml                      # Orquestador de la infraestructura (API + BD)
├── Dockerfile                              # Receta de construcción de la imagen Python/Alpine
├── requirements.txt                        # Lista de dependencias del proyecto
└── README.md                               # Documentación general y técnica
```

