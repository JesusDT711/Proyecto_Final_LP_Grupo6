# Backend en Python - Veterinaria Huellitas

Backend desarrollado en Python siguiendo una arquitectura por capas desacoplada (equivalente a la arquitectura Spring Boot en Java del proyecto de referencia).

## Módulo `modelo/` (Entidades de Dominio / ORM)

Mapea fielmente el esquema de base de datos MySQL definido en `veterinaria_huellitas.sql`:

| Entidad / Archivo | Tabla en BD | Descripción | Relaciones Clave |
|---|---|---|---|
| [`Rol`](modelo/rol.py) | `roles` | Roles de usuario (`ADMIN`, `CLIENTE`). | 1 a N con `usuarios` |
| [`Usuario`](modelo/usuario.py) | `usuarios` | Usuarios del sistema con email único, contraseña encriptada, datos personales y teléfono. | N a 1 con `roles`, 1 a N con `mascotas`, 1 a N con `reservas`, 1 a N con `atenciones` (staff) |
| [`Mascota`](modelo/mascota.py) | `mascotas` | Mascotas pertenecientes a un cliente. Incorporada según la normalización del script SQL. | N a 1 con `usuarios` (ON DELETE CASCADE), 1 a N con `reservas` (ON DELETE RESTRICT) |
| [`Servicio`](modelo/servicio.py) | `servicios` | Servicios ofrecidos (precio, duración en minutos, baja lógica con `activo`). | 1 a N con `reservas` |
| [`EstadoReserva`](modelo/estado_reserva.py) | `ENUM(...)` | Estados: `CONFIRMADA`, `CANCELADA`, `ATENDIDA`. | Utilizado en `reservas` |
| [`Reserva`](modelo/reserva.py) | `reservas` | Cita agendada con hora de inicio y fin (duración calculada), observaciones y estado. | N a 1 con `mascotas`, N a 1 con `usuarios`, N a 1 con `servicios`, 1 a 1 con `atenciones` |
| [`Atencion`](modelo/atencion.py) | `atenciones` | Expediente clínico resultante de una cita atendida. | 1 a 1 con `reservas` (`reserva_id UNIQUE`), N a 1 con `usuarios` (`atendido_por_id`) |

### Mejoras y Adaptaciones respecto al Modelo Java:
1. **Entidad Mascota Normalizada:** A diferencia del proyecto Java donde el nombre de la mascota era solo un campo de texto plano dentro de la reserva, el modelo en Python implementa la entidad completa `Mascota` vinculada al `Usuario` cliente con cascada de eliminación.
2. **Entidad Atención (Expediente Clínico):** Mapea la tabla `atenciones` con relación 1 a 1 hacia `Reserva` y registro del personal médico (`atendido_por_id`).
3. **Serialización universal (`to_dict`):** Cada clase implementa serialización nativa a diccionario con formato dual (camelCase y snake_case) para compatibilidad inmediata con el Frontend en Angular / TypeScript y con APIs REST.
4. **Protección de datos sensibles:** En `Usuario.to_dict()`, el campo `password` se omite por defecto para evitar filtración de contraseñas.
5. **Compatibilidad Dual:** Diseñado con SQLAlchemy 2.0 y compatibilidad pura de objetos Python (POPO).

## Verificación de los Modelos

Para ejecutar la suite de prueba de los modelos:
```bash
python verificar_modelos.py
```

