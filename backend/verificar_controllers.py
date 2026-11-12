"""
Script de verificación y pruebas de las capas Controller y DTO de Veterinaria Huellitas.
Prueba el ciclo de petición y respuesta HTTP (status code, DTOs y validación).
"""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Configurar rutas para ejecución independiente
backend_dir = Path(__file__).resolve().parent
repo_dir = backend_dir.parent
for p in [str(backend_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

# Repositorios
from repository import (
    AtencionRepository,
    MascotaRepository,
    ReservaRepository,
    RolRepository,
    ServicioRepository,
    UsuarioRepository,
)

# Servicios
from service import (
    AtencionService,
    AuthService,
    HorarioAtencion,
    MascotaService,
    ReservaService,
    ServicioService,
    UsuarioService,
)

# DTOs
from dto import (
    AtencionRequest,
    AtencionResponse,
    AuthResponse,
    LoginRequest,
    MascotaRequest,
    MascotaResponse,
    MensajeResponse,
    RegistroRequest,
    ReservaRequest,
    ReservaResponse,
    ServicioRequest,
    ServicioResponse,
    UsuarioResponse,
    UsuarioUpdateRequest,
)

# Controladores
from controller import (
    ApiResponse,
    AtencionController,
    AuthController,
    MascotaController,
    ReservaAdminController,
    ReservaController,
    ServicioController,
    UsuarioAdminController,
)

from model import Rol


def probar_controllers():
    print("=" * 70)
    print("INICIANDO PRUEBAS DE LAS CAPAS DTO Y CONTROLLER")
    print("=" * 70)

    # 1. Configuración de dependencias
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

    # Inicializar Controladores
    auth_ctrl = AuthController(auth_service)
    servicio_ctrl = ServicioController(servicio_service)
    mascota_ctrl = MascotaController(mascota_service)
    reserva_ctrl = ReservaController(reserva_service)
    reserva_admin_ctrl = ReservaAdminController(reserva_service)
    usuario_admin_ctrl = UsuarioAdminController(usuario_service)
    atencion_ctrl = AtencionController(atencion_service)

    # -------------------------------------------------------------
    # 1. AuthController (Registro y Login)
    # -------------------------------------------------------------
    print("\n[1] Probando AuthController...")

    # POST /api/auth/registro -> 201 Created
    reg_dto = RegistroRequest(
        nombreCompleto="Sofia Martinez",
        email="sofia.martinez@gmail.com",
        password="sofia_password_123",
        telefono="955112233",
    )
    res_reg = auth_ctrl.registrar(reg_dto)
    assert res_reg.status_code == 201
    assert isinstance(res_reg.data, MensajeResponse)
    print(f"  ✓ POST /api/auth/registro: HTTP {res_reg.status_code} - {res_reg.data.mensaje}")

    # POST /api/auth/login -> 200 OK
    login_dto = LoginRequest(email="sofia.martinez@gmail.com", password="sofia_password_123")
    res_login = auth_ctrl.login(login_dto)
    assert res_login.status_code == 200
    assert isinstance(res_login.data, AuthResponse)
    assert res_login.data.rol == "CLIENTE"
    token_jwt = res_login.data.token
    print(f"  ✓ POST /api/auth/login: HTTP {res_login.status_code} - Token generado correctamente")

    # Crear staff veterinario (ADMIN) para pruebas
    vet_user = usuario_repo.guardar(
        usuario_repo.model_class(
            email="dra.valeria@huellitas.com",
            password="hash_admin_vet",
            nombre_completo="Dra. Valeria Gomez",
            rol_id=rol_admin.id,
        )
    )
    vet_user.rol = rol_admin

    # -------------------------------------------------------------
    # 2. ServicioController (Catálogo de Servicios)
    # -------------------------------------------------------------
    print("\n[2] Probando ServicioController...")

    # POST /api/servicios -> 201 Created
    srv_dto = ServicioRequest(
        nombre="Vacunación Antirrábica",
        descripcion="Inmunización obligatoria anual",
        precio=45.00,
        duracionMinutos=20,
    )
    res_srv_crear = servicio_ctrl.crear(srv_dto)
    assert res_srv_crear.status_code == 201
    assert isinstance(res_srv_crear.data, ServicioResponse)
    servicio_id = res_srv_crear.data.id
    print(f"  ✓ POST /api/servicios: HTTP {res_srv_crear.status_code} - Servicio #{servicio_id}: {res_srv_crear.data.nombre}")

    # GET /api/servicios -> 200 OK
    res_srv_list = servicio_ctrl.listar()
    assert res_srv_list.status_code == 200
    assert len(res_srv_list.data) >= 1
    print(f"  ✓ GET /api/servicios: HTTP {res_srv_list.status_code} - {len(res_srv_list.data)} servicio(s) activo(s)")

    # GET /api/servicios/buscar?nombre=antirrábica
    res_srv_buscar = servicio_ctrl.buscar("antirrábica")
    assert res_srv_buscar.status_code == 200
    assert len(res_srv_buscar.data) == 1
    print(f"  ✓ GET /api/servicios/buscar: HTTP {res_srv_buscar.status_code} - Búsqueda exitosa")

    # PUT /api/servicios/{id} -> 200 OK
    srv_mod_dto = ServicioRequest(
        nombre="Vacunación Antirrábica Reforzada",
        precio=50.00,
        duracionMinutos=25,
        descripcion="Incluye desparasitación",
    )
    res_srv_act = servicio_ctrl.actualizar(servicio_id, srv_mod_dto)
    assert res_srv_act.status_code == 200
    assert res_srv_act.data.nombre == "Vacunación Antirrábica Reforzada"
    print(f"  ✓ PUT /api/servicios/{servicio_id}: HTTP {res_srv_act.status_code} - Actualizado")

    # -------------------------------------------------------------
    # 3. MascotaController (Mascotas del Cliente)
    # -------------------------------------------------------------
    print("\n[3] Probando MascotaController...")

    # POST /api/mascotas -> 201 Created
    masc_dto = MascotaRequest(
        nombre="Luna",
        especie="Felino",
        raza="Siamés",
        sexo="Hembra",
        fechaNacimiento="2023-01-15",
    )
    res_masc = mascota_ctrl.registrar(masc_dto, email_cliente="sofia.martinez@gmail.com")
    assert res_masc.status_code == 201
    assert isinstance(res_masc.data, MascotaResponse)
    mascota_id = res_masc.data.id
    print(f"  ✓ POST /api/mascotas: HTTP {res_masc.status_code} - Mascota #{mascota_id}: {res_masc.data.nombre}")

    # GET /api/mascotas/mis-mascotas -> 200 OK
    res_mis_masc = mascota_ctrl.mis_mascotas(email_cliente="sofia.martinez@gmail.com")
    assert res_mis_masc.status_code == 200
    assert len(res_mis_masc.data) == 1
    print(f"  ✓ GET /api/mascotas/mis-mascotas: HTTP {res_mis_masc.status_code} - {len(res_mis_masc.data)} mascota(s)")

    # -------------------------------------------------------------
    # 4. ReservaController y ReservaAdminController
    # -------------------------------------------------------------
    print("\n[4] Probando ReservaController y ReservaAdminController...")

    # Calcular fecha futura hábil (11:00 AM)
    fecha_futura = datetime.now() + timedelta(days=4)
    fecha_futura = fecha_futura.replace(hour=11, minute=0, second=0, microsecond=0)
    if fecha_futura.weekday() == 6:  # Si cae domingo, mover a lunes
        fecha_futura += timedelta(days=1)

    # POST /api/reservas -> 201 Created (Nace CONFIRMADA)
    reserva_dto = ReservaRequest(
        servicioId=servicio_id,
        fechaHora=fecha_futura.isoformat(),
        mascotaId=mascota_id,
        observaciones="Cita periódica",
    )
    res_reserva = reserva_ctrl.crear(reserva_dto, email_cliente="sofia.martinez@gmail.com")
    assert res_reserva.status_code == 201
    assert isinstance(res_reserva.data, ReservaResponse)
    assert res_reserva.data.estado == "CONFIRMADA"
    reserva_id = res_reserva.data.id
    print(f"  ✓ POST /api/reservas: HTTP {res_reserva.status_code} - Reserva #{reserva_id} ({res_reserva.data.estado})")

    # GET /api/reservas/mis-reservas -> 200 OK
    res_historial = reserva_ctrl.mis_reservas("sofia.martinez@gmail.com")
    assert res_historial.status_code == 200
    assert len(res_historial.data) == 1
    print(f"  ✓ GET /api/reservas/mis-reservas: HTTP {res_historial.status_code} - Historial cliente consultado")

    # GET /api/admin/reservas?estado=CONFIRMADA -> 200 OK
    res_admin_list = reserva_admin_ctrl.listar(estado="CONFIRMADA")
    assert res_admin_list.status_code == 200
    print(f"  ✓ GET /api/admin/reservas: HTTP {res_admin_list.status_code} - {len(res_admin_list.data)} confirmada(s)")

    # -------------------------------------------------------------
    # 5. AtencionController (Expediente Médico)
    # -------------------------------------------------------------
    print("\n[5] Probando AtencionController...")

    # POST /api/atenciones -> 201 Created
    aten_dto = AtencionRequest(
        reservaId=reserva_id,
        diagnosticoODetalle="Paciente felino en óptimas condiciones corporales.",
        tratamientoOIndicaciones="Dosis única de refuerzo antirrábico aplicada.",
        pesoKg=4.2,
    )
    res_atencion = atencion_ctrl.registrar(aten_dto, email_veterinario="dra.valeria@huellitas.com")
    assert res_atencion.status_code == 201
    assert isinstance(res_atencion.data, AtencionResponse)
    assert res_atencion.data.peso_kg == 4.2
    print(f"  ✓ POST /api/atenciones: HTTP {res_atencion.status_code} - Expediente #{res_atencion.data.id} creado")

    # GET /api/atenciones/reserva/{reserva_id} -> 200 OK
    res_aten_cons = atencion_ctrl.obtener_por_reserva(reserva_id)
    assert res_aten_cons.status_code == 200
    assert res_aten_cons.data.diagnostico_o_detalle == "Paciente felino en óptimas condiciones corporales."
    print(f"  ✓ GET /api/atenciones/reserva/{reserva_id}: HTTP {res_aten_cons.status_code} - Consulta exitosa")

    # -------------------------------------------------------------
    # 6. UsuarioAdminController (Gestión de Usuarios)
    # -------------------------------------------------------------
    print("\n[6] Probando UsuarioAdminController...")

    # GET /api/admin/usuarios -> 200 OK
    res_users = usuario_admin_ctrl.listar()
    assert res_users.status_code == 200
    assert len(res_users.data) >= 2
    print(f"  ✓ GET /api/admin/usuarios: HTTP {res_users.status_code} - {len(res_users.data)} usuario(s)")

    # GET /api/admin/usuarios/{id} -> 200 OK
    cliente_id = [u.id for u in res_users.data if u.email == "sofia.martinez@gmail.com"][0]
    res_user_det = usuario_admin_ctrl.obtener(cliente_id)
    assert res_user_det.status_code == 200
    assert res_user_det.data.email == "sofia.martinez@gmail.com"
    print(f"  ✓ GET /api/admin/usuarios/{cliente_id}: HTTP {res_user_det.status_code} - {res_user_det.data.nombreCompleto}")

    # PUT /api/admin/usuarios/{id} -> 200 OK
    mod_user_dto = UsuarioUpdateRequest(
        nombreCompleto="Sofia Martinez de la Torre",
        email="sofia.martinez@gmail.com",
        telefono="944332211",
    )
    res_mod_u = usuario_admin_ctrl.actualizar(cliente_id, mod_user_dto, email_solicitante="dra.valeria@huellitas.com")
    assert res_mod_u.status_code == 200
    assert res_mod_u.data.nombreCompleto == "Sofia Martinez de la Torre"
    print(f"  ✓ PUT /api/admin/usuarios/{cliente_id}: HTTP {res_mod_u.status_code} - Actualizado correctamente")

    print("\n" + "=" * 70)
    print("¡TODAS LAS PRUEBAS DE DTO Y CONTROLLER PASARON EXITOSAMENTE!")
    print("=" * 70)


if __name__ == "__main__":
    probar_controllers()

