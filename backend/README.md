# Backend en Python - Veterinaria Huellitas

Backend desarrollado en Python siguiendo una arquitectura limpia por capas desacoplada (equivalente a la arquitectura Spring Boot en Java del proyecto modelo de referencia).

## Estructura del Backend

```text
backend/
├── model/                # Capa de Entidades de Dominio (ORM)
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
├── exception/            # Excepciones de negocio personalizadas
│   └── api_exception.py
├── util/                 # Utilidades (normalización de email, hash de claves, JWT)
│   ├── email_util.py
│   └── seguridad_util.py
├── requirements.txt      # Dependencias del backend
├── verificar_modelos.py  # Test de entidades
└── verificar_servicios.py # Test integral de repositorios y servicios
```

---

## 1. Módulo `repository/` (Acceso a Datos)

Equivalente a las interfaces `JpaRepository` del proyecto de referencia en Java, con soporte para sesiones de base de datos MySQL (SQLAlchemy) y fallback en memoria para tests unitarios:

| Repositorio | Entidad | Métodos Clave |
|---|---|---|
| [`RolRepository`](repository/rol_repository.py) | `Rol` | `buscar_por_nombre(nombre)` |
| [`UsuarioRepository`](repository/usuario_repository.py) | `Usuario` | `buscar_por_email(email)`, `existe_por_email(email)`, `existe_por_email_y_distinto_id(email, id)` |
| [`MascotaRepository`](repository/mascota_repository.py) | `Mascota` | `listar_por_usuario(usuario_id)`, `buscar_por_id_y_usuario(id, usuario_id)`, `existe_por_usuario(usuario_id)` |
| [`ServicioRepository`](repository/servicio_repository.py) | `Servicio` | `listar_activos()`, `buscar_por_nombre(nombre)`, `existe_por_nombre_ignore_case(nombre)`, `existe_por_nombre_ignore_case_y_distinto_id(...)` |
| [`ReservaRepository`](repository/reserva_repository.py) | `Reserva` | `historial_por_usuario(usuario_id)`, `listar_todas()`, `listar_por_estado(estado)`, `contar_cruces(servicio_id, estado, inicio, fin)`, `existe_por_usuario(...)`, `existe_por_mascota(...)` |
| [`AtencionRepository`](repository/atencion_repository.py) | `Atencion` | `buscar_por_reserva_id(reserva_id)`, `existe_por_reserva_id(...)`, `listar_por_veterinario(...)` |

---

## 2. Módulo `service/` (Lógica de Negocio)

Implementa fielmente las reglas de negocio de la clínica:

1. **[`HorarioAtencion`](service/horario_atencion.py):** Atiende de Lunes a Sábado de 09:00 a 21:00 (Domingos cerrado). Valida que la cita inicie y concluya estrictamente dentro del horario comercial.
2. **[`AuthService`](service/auth_service.py):** Registro público exclusivo para rol `CLIENTE`, normalización de correos (`EmailUtil`), encriptación de claves (`SeguridadUtil`), validación de duplicados y generación de JWT en login.
3. **[`UsuarioService`](service/usuario_service.py):** Panel de administración para usuarios: listar, actualizar, impedir auto-degradación de rol del admin logueado, e impedir eliminación de usuarios con reservas históricas.
4. **[`ServicioService`](service/servicio_service.py):** CRUD de servicios veterinarios, unicidad de nombre y baja lógica con `activo = False`.
5. **[`MascotaService`](service/mascota_service.py):** Registro y consulta de mascotas por cliente titular, asegurando control de acceso para que clientes ajenos no puedan manipular datos de otras mascotas.
6. **[`ReservaService`](service/reserva_service.py):** 
   - **Confirmación automática:** Nace en estado `CONFIRMADA` sin necesidad de intervención de un administrador si el servicio está activo, la fecha es futura, está dentro del horario y no existe cruce horario.
   - **Cancelación:** Solo permitida al cliente dueño con al menos 24 horas de anticipación.
   - **Supervisión administrativa:** Listado global y marcado a `ATENDIDA`.
7. **[`AtencionService`](service/atencion_service.py):** Registro del expediente médico veterinario (peso, diagnóstico, tratamiento) con relación 1 a 1 y cambio automático de la cita a `ATENDIDA`.

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
