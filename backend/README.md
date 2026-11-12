# Backend en Python - Veterinaria Huellitas

Backend desarrollado en Python siguiendo una arquitectura limpia por capas desacoplada (equivalente a la arquitectura Spring Boot en Java del proyecto modelo de referencia).

## Estructura del Backend

```text
backend/
├── __init__.py           # Paquete raíz de backend (gestión de rutas e imports)
├── model/                # Capa de Entidades de Dominio (ORM / SQLAlchemy)
│   ├── base.py
│   ├── estado_reserva.py
│   ├── rol.py
│   ├── usuario.py
│   ├── mascota.py
│   ├── servicio.py
│   ├── reserva.py
│   └── atencion.py
├── repository/           # Capa de Acceso a Datos (DAO / Repositorios)
│   ├── base_repository.py
│   ├── rol_repository.py
│   ├── usuario_repository.py
│   ├── mascota_repository.py
│   ├── servicio_repository.py
│   ├── reserva_repository.py
│   └── atencion_repository.py
├── service/              # Capa de Lógica de Negocio
│   ├── horario_atencion.py
│   ├── auth_service.py
│   ├── usuario_service.py
│   ├── servicio_service.py
│   ├── mascota_service.py
│   ├── reserva_service.py
│   └── atencion_service.py
├── dto/                  # Capa de Transferencia de Datos (Request / Response)
│   ├── base_dto.py
│   ├── auth_dto.py
│   ├── usuario_dto.py
│   ├── servicio_dto.py
│   ├── mascota_dto.py
│   ├── reserva_dto.py
│   └── atencion_dto.py
├── controller/           # Capa de Controladores REST (Endpoints / API)
│   ├── base_controller.py
│   ├── auth_controller.py
│   ├── servicio_controller.py
│   ├── reserva_controller.py
│   ├── reserva_admin_controller.py
│   ├── usuario_admin_controller.py
│   ├── mascota_controller.py
│   └── atencion_controller.py
├── exception/            # Excepciones de negocio personalizadas
│   └── api_exception.py
├── util/                 # Utilidades (normalización de email, hash de claves, JWT)
│   ├── email_util.py
│   └── seguridad_util.py
├── requirements.txt      # Dependencias del backend
├── verificar_modelos.py  # Test de entidades
├── verificar_servicios.py # Test de repositorios y lógica de negocio
└── verificar_controllers.py # Test de DTOs y controladores REST
```

---

## 1. Módulo `dto/` (Data Transfer Objects)

Modelos de validación y transferencia de datos que desacoplan la capa de presentación de las entidades ORM:

| DTO | Propósito | Equivalente en Java |
|---|---|---|
| `RegistroRequest` / `LoginRequest` | Datos de entrada para registrarse e iniciar sesión. | `RegistroRequest.java`, `LoginRequest.java` |
| `AuthResponse` | Retorna el token JWT y datos de sesión del usuario. | `AuthResponse.java` |
| `MensajeResponse` | Mensaje genérico de respuesta (`{"mensaje": "..."}`). | `MensajeResponse.java` |
| `ServicioRequest` / `ServicioResponse` | Entrada y salida para catálogo de servicios veterinarios. | `ServicioRequest.java`, `ServicioResponse.java` |
| `ReservaRequest` / `ReservaResponse` | Datos para agendar cita y respuesta con detalle de fecha, servicio y mascota. | `ReservaRequest.java`, `ReservaResponse.java` |
| `MascotaRequest` / `MascotaResponse` | Datos de entrada y salida para el perfil de mascotas. | *(Nueva en SQL normalizado)* |
| `AtencionRequest` / `AtencionResponse` | Registro de expediente médico (peso, diagnóstico y tratamiento). | *(Nueva en SQL normalizado)* |
| `UsuarioUpdateRequest` / `UsuarioResponse`| Modificación y consulta de cuentas de usuario por el administrador. | `UsuarioUpdateRequest.java`, `UsuarioResponse.java` |

---

## 2. Módulo `controller/` (Controladores REST)

Implementa los endpoints de la API devolviendo objetos `ApiResponse` que encapsulan el cuerpo y el código de estado HTTP (`ResponseEntity` de Spring Boot):

| Controlador | Ruta Base | Métodos / Endpoints | Rol Requerido |
|---|---|---|---|
| [`AuthController`](controller/auth_controller.py) | `/api/auth` | `POST /registro` (201), `POST /login` (200) | Público |
| [`ServicioController`](controller/servicio_controller.py) | `/api/servicios` | `GET /` (200), `GET /buscar` (200), `GET /{id}` (200), `POST /` (201), `PUT /{id}` (200), `DELETE /{id}` (200) | Lectura: Todos / Escritura: ADMIN |
| [`ReservaController`](controller/reserva_controller.py) | `/api/reservas` | `POST /` (201), `GET /mis-reservas` (200), `PUT /{id}/cancelar` (200) | CLIENTE |
| [`ReservaAdminController`](controller/reserva_admin_controller.py) | `/api/admin/reservas` | `GET /` (200), `PUT /{id}/atendida` (200) | ADMIN |
| [`MascotaController`](controller/mascota_controller.py) | `/api/mascotas` | `POST /` (201), `GET /mis-mascotas` (200), `GET /{id}` (200), `PUT /{id}` (200), `DELETE /{id}` (200) | CLIENTE / ADMIN |
| [`AtencionController`](controller/atencion_controller.py) | `/api/atenciones` | `POST /` (201), `GET /reserva/{id}` (200), `GET /mis-atenciones` (200) | ADMIN (Personal médico) |
| [`UsuarioAdminController`](controller/usuario_admin_controller.py) | `/api/admin/usuarios` | `GET /` (200), `GET /{id}` (200), `PUT /{id}` (200), `DELETE /{id}` (200) | ADMIN |

---

## Ejecución de Pruebas

Para validar los modelos:
```bash
python verificar_modelos.py
```

Para validar los repositorios y servicios con sus reglas de negocio:
```bash
python verificar_servicios.py
```

Para validar los controladores y el flujo completo de peticiones REST:
```bash
python verificar_controllers.py
```
