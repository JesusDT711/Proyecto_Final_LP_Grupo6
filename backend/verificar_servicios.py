
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
repo_dir = backend_dir.parent
if str(repo_dir) not in sys.path:
    sys.path.insert(0, str(repo_dir))
if str(backend_dir) not in sys.path:
    sys.path.insert(1, str(backend_dir))

from datetime import date, datetime, timedelta
from decimal import Decimal

try:
    from repository import (
        RolRepository,
        UsuarioRepository,
        MascotaRepository,
        ServicioRepository,
        ReservaRepository,
        AtencionRepository,
    )
    from service import (
        HorarioAtencion,
        AuthService,
        UsuarioService,
        ServicioService,
        MascotaService,
        ReservaService,
        AtencionService,
    )
    from exception import ApiException
    from model import EstadoReserva, Rol
except ImportError:
    from backend.repository import (
        RolRepository,
        UsuarioRepository,
        MascotaRepository,
        ServicioRepository,
        ReservaRepository,
        AtencionRepository,
    )
    from backend.service import (
        HorarioAtencion,
        AuthService,
        UsuarioService,
        ServicioService,
        MascotaService,
        ReservaService,
        AtencionService,
    )
    from backend.exception import ApiException
    from backend.model import EstadoReserva, Rol



def probar_servicios():
    print("=" * 70)
    print("INICIANDO PRUEBAS DE LAS CAPAS REPOSITORY Y SERVICE")
    print("=" * 70)

    # Inicializar repositorios en memoria
    rol_repo = RolRepository()
    usuario_repo = UsuarioRepository()
    mascota_repo = MascotaRepository()
    servicio_repo = ServicioRepository()
    reserva_repo = ReservaRepository()
    atencion_repo = AtencionRepository()

    rol_admin = rol_repo.guardar(Rol(nombre="ADMIN"))
    rol_cliente = rol_repo.guardar(Rol(nombre="CLIENTE"))

    auth_service = AuthService(usuario_repo, rol_repo)
    usuario_service = UsuarioService(usuario_repo, rol_repo, reserva_repo)
    servicio_service = ServicioService(servicio_repo)
    mascota_service = MascotaService(mascota_repo, usuario_repo, reserva_repo)
    reserva_service = ReservaService(reserva_repo, servicio_repo, usuario_repo, mascota_repo)
    atencion_service = AtencionService(atencion_repo, reserva_repo, usuario_repo)

    print("\n[1] Probando AuthService...")

    res_reg = auth_service.registrar(
        nombre_completo="Juan Perez",
        email="juan.perez@gmail.com",
        password="password123",
        telefono="987654321",
    )
    assert res_reg["mensaje"] == "Usuario registrado correctamente"
    print("  ✓ Registro de cliente exitoso")

    try:
        auth_service.registrar(
            nombre_completo="Juan Perez",
            email="juan.perez@gmail.com",
            password="password123",
        )
        assert False, "Debería haber lanzado error de correo duplicado"
    except ApiException as e:
        assert e.status_code == 409
        print(f"  ✓ Conflicto de correo duplicado detectado: {e.mensaje}")

    auth_data = auth_service.login("juan.perez@gmail.com", "password123")
    assert "token" in auth_data and auth_data["rol"] == "CLIENTE"
    print(f"  ✓ Login exitoso. Token JWT generado para: {auth_data['nombreCompleto']}")

    try:
        auth_service.login("juan.perez@gmail.com", "clave_incorrecta")
        assert False, "Debería haber lanzado 401"
    except ApiException as e:
        assert e.status_code == 401
        print("  ✓ Credenciales inválidas rechazadas correctamente (401)")

    admin_user = usuario_repo.guardar(
        usuario_repo.model_class(
            email="admin@huellitas.com",
            password="admin_hash_123",
            nombre_completo="Dr. Martin Veterinaria",
            rol_id=rol_admin.id,
        )
    )
    admin_user.rol = rol_admin

    print("\n[2] Probando ServicioService...")

    srv1 = servicio_service.crear(
        nombre="Consulta Médica General",
        descripcion="Revisión integral",
        precio=60.00,
        duracion_minutos=30,
    )
    assert srv1["id"] is not None
    print(f"  ✓ Servicio creado: {srv1['nombre']} (Duración: {srv1['duracionMinutos']} min)")

    try:
        servicio_service.crear("consulta médica general", 50.0, 30)
        assert False
    except ApiException as e:
        assert e.status_code == 409
        print(f"  ✓ Validación de nombre duplicado: {e.mensaje}")

    res_des = servicio_service.desactivar(srv1["id"])
    assert res_des["mensaje"] == "Servicio desactivado correctamente"
    srv1_actual = servicio_service.obtener(srv1["id"])
    assert srv1_actual["activo"] is False
    print("  ✓ Baja lógica aplicada: activo = False")

    servicio_service.actualizar(srv1["id"], srv1["nombre"], srv1["precio"], srv1["duracionMinutos"], activo=True)

    print("\n[3] Probando MascotaService...")

    mascota1 = mascota_service.registrar(
        email_cliente="juan.perez@gmail.com",
        nombre="Rocky",
        especie="Canino",
        raza="Labrador",
        sexo="Macho",
        fecha_nacimiento=date(2022, 3, 10),
    )
    assert mascota1["id"] is not None
    print(f"  ✓ Mascota registrada: {mascota1['nombre']} (Dueño: {mascota1['propietarioNombre']})")

    mascotas_juan = mascota_service.listar_por_dueno("juan.perez@gmail.com")
    assert len(mascotas_juan) == 1
    print(f"  ✓ Listado de mascotas del cliente: {len(mascotas_juan)} encontrada(s)")

    print("\n[4] Probando ReservaService y Reglas de Negocio...")

    ahora = datetime.now()
    dias_adelanto = 5
    fecha_cita = ahora + timedelta(days=dias_adelanto)
    fecha_cita = fecha_cita.replace(hour=10, minute=0, second=0, microsecond=0)
    if fecha_cita.weekday() == 6:
        fecha_cita += timedelta(days=1)

    reserva1 = reserva_service.crear(
        email_cliente="juan.perez@gmail.com",
        servicio_id=srv1["id"],
        fecha_hora=fecha_cita,
        mascota_id=mascota1["id"],
        observaciones="Primera visita",
    )
    assert reserva1["estado"] == "CONFIRMADA"
    print(f"  ✓ Reserva agendada exitosamente con estado: {reserva1['estado']}")
    print(f"    Horario: {reserva1['fechaHora']} hasta {reserva1['fechaHoraFin']}")

    try:
        reserva_service.crear(
            email_cliente="juan.perez@gmail.com",
            servicio_id=srv1["id"],
            fecha_hora=fecha_cita + timedelta(minutes=10),
            mascota_id=mascota1["id"],
        )
        assert False, "Debería haber detectado solapamiento de horario"
    except ApiException as e:
        assert e.status_code == 409
        print(f"  ✓ Detección de solapamiento de horario confirmada: {e.mensaje}")

    proximo_domingo = ahora + timedelta(days=(6 - ahora.weekday() + 7) % 7 or 7)
    proximo_domingo = proximo_domingo.replace(hour=10, minute=0, second=0, microsecond=0)
    try:
        reserva_service.crear(
            email_cliente="juan.perez@gmail.com",
            servicio_id=srv1["id"],
            fecha_hora=proximo_domingo,
            mascota_id=mascota1["id"],
        )
        assert False
    except ApiException as e:
        assert e.status_code == 400
        print(f"  ✓ Regla de horario de domingo respetada: {e.mensaje}")

    try:
        reserva_service.cancelar(reserva1["id"], email_solicitante="otro_cliente@gmail.com")
        assert False
    except ApiException as e:
        assert e.status_code == 403
        print("  ✓ Intento de cancelación por usuario ajeno bloqueado (403 Forbidden)")

    res_cancelada = reserva_service.cancelar(reserva1["id"], email_solicitante="juan.perez@gmail.com")
    assert res_cancelada["estado"] == "CANCELADA"
    print(f"  ✓ Cancelación anticipada exitosa. Nuevo estado: {res_cancelada['estado']}")

    print("\n[5] Probando AtencionService (Expediente Médico)...")

    otra_fecha = fecha_cita + timedelta(hours=2)
    reserva2 = reserva_service.crear(
        email_cliente="juan.perez@gmail.com",
        servicio_id=srv1["id"],
        fecha_hora=otra_fecha,
        mascota_id=mascota1["id"],
    )

    atencion1 = atencion_service.registrar_atencion(
        email_veterinario="admin@huellitas.com",
        reserva_id=reserva2["id"],
        diagnostico_o_detalle="Se detecta ligera otitis externa.",
        tratamiento_o_indicaciones="Gotas óticas cada 12 horas por 7 días.",
        peso_kg=32.4,
    )
    assert atencion1["id"] is not None
    assert atencion1["pesoKg"] == 32.4
    print(f"  ✓ Atención registrada con éxito (Expediente #{atencion1['id']})")

    reserva2_check = reserva_service._buscar_reserva(reserva2["id"])
    assert reserva2_check.estado == EstadoReserva.ATENDIDA
    print("  ✓ Estado de la reserva actualizado automáticamente a 'ATENDIDA'")

    try:
        atencion_service.registrar_atencion(
            email_veterinario="admin@huellitas.com",
            reserva_id=reserva2["id"],
            diagnostico_o_detalle="Intento duplicado",
        )
        assert False
    except ApiException as e:
        assert e.status_code == 409
        print(f"  ✓ Relación 1 a 1 protegida contra expedientes duplicados: {e.mensaje}")

    atencion_cons = atencion_service.obtener_por_reserva(reserva2["id"])
    assert atencion_cons["diagnosticoODetalle"] == "Se detecta ligera otitis externa."
    print("  ✓ Consulta de expediente clínico por reserva validada")

    print("\n" + "=" * 70)
    print("¡TODAS LAS PRUEBAS DE REPOSITORY Y SERVICE PASARON EXITOSAMENTE!")
    print("=" * 70)

if __name__ == "__main__":
    probar_servicios()
