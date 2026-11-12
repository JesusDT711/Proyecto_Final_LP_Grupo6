"""
Script de verificación y pruebas de las capas Config y Security de Veterinaria Huellitas.
Prueba la configuración general, conexión a BD, tokens JWT, filtros de seguridad y reglas de acceso.
"""

import sys
from pathlib import Path

# Configurar rutas
backend_dir = Path(__file__).resolve().parent
repo_dir = backend_dir.parent
for p in [str(backend_dir), str(repo_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from config import (
    SQLALCHEMY_AVAILABLE,
    Settings,
    get_db,
    get_engine,
    settings,
)
from exception import ApiException
from model import Rol, Usuario
from repository import RolRepository, UsuarioRepository
from security import (
    JwtService,
    SecurityConfig,
    SecurityFilter,
    UserDetails,
    UserDetailsService,
    requerir_admin,
    requerir_autenticacion,
    requerir_cliente,
)


def probar_security_y_config():
    print("=" * 70)
    print("INICIANDO PRUEBAS DE LAS CAPAS CONFIG Y SECURITY")
    print("=" * 70)

    # -------------------------------------------------------------
    # 1. Pruebas de Configuración (Settings y Database)
    # -------------------------------------------------------------
    print("\n[1] Probando Config (settings y database)...")

    assert settings.APP_NAME == "Veterinaria Huellitas Backend"
    assert settings.TIMEZONE == "America/Lima"
    assert settings.HORARIO_APERTURA == "09:00"
    assert settings.HORARIO_CIERRE == "21:00"
    assert "veterinaria_huellitas" in settings.DATABASE_URL
    print(f"  ✓ Settings cargados: {settings.APP_NAME} (Zona horaria: {settings.TIMEZONE})")
    print(f"  ✓ URL de BD configurada: {settings.DATABASE_URL}")
    print(f"  ✓ Horario de atención configurado: {settings.HORARIO_APERTURA} a {settings.HORARIO_CIERRE}")
    print(f"  ✓ Soporte SQLAlchemy activo: {SQLALCHEMY_AVAILABLE}")

    # Probar inyección de sesión con get_db()
    for session in get_db():
        # session puede ser None si no hay base de datos física levantada, lo cual es normal en tests desacoplados
        print("  ✓ Generador get_db() evaluado correctamente")
        break

    # -------------------------------------------------------------
    # 2. Pruebas de JwtService
    # -------------------------------------------------------------
    print("\n[2] Probando JwtService...")

    jwt_service = JwtService(secret_key="clave_test_huellitas_2026", expiracion_horas=2)

    # Generar token
    token = jwt_service.generar_token(
        email="cliente.test@gmail.com",
        rol="CLIENTE",
        nombre_completo="Carlos Prueba",
    )
    assert token and isinstance(token, str)
    print("  ✓ Token JWT firmado generado con éxito")

    # Validar token
    payload = jwt_service.validar_token(token)
    assert payload is not None
    assert payload.get("email") == "cliente.test@gmail.com"
    assert payload.get("rol") == "CLIENTE"
    print(f"  ✓ Token validado: email={payload.get('email')}, rol={payload.get('rol')}")

    # Rechazo de token adulterado
    token_falso = token + "modificado"
    assert jwt_service.validar_token(token_falso) is None
    print("  ✓ Token alterado rechazado correctamente")

    # -------------------------------------------------------------
    # 3. Pruebas de UserDetails y UserDetailsService
    # -------------------------------------------------------------
    print("\n[3] Probando UserDetails y UserDetailsService...")

    user_details_admin = UserDetails(
        id=1,
        email="admin@huellitas.com",
        nombre_completo="Dr. Fernando Admin",
        rol="ADMIN",
    )
    assert user_details_admin.es_admin() is True
    assert user_details_admin.es_cliente() is False
    print("  ✓ UserDetails (ADMIN) verificado")

    user_details_cli = UserDetails(
        id=2,
        email="carlos@gmail.com",
        nombre_completo="Carlos Cliente",
        rol="CLIENTE",
    )
    assert user_details_cli.es_cliente() is True
    assert user_details_cli.es_admin() is False
    print("  ✓ UserDetails (CLIENTE) verificado")

    # Configurar repositorio de usuarios en memoria
    rol_repo = RolRepository()
    usuario_repo = UsuarioRepository()
    rol_admin = rol_repo.guardar(Rol(id=1, nombre="ADMIN"))
    u_admin = usuario_repo.guardar(
        Usuario(
            id=10,
            email="dra.lucia@huellitas.com",
            password="hash",
            nombre_completo="Dra. Lucia",
            rol_id=rol_admin.id,
        )
    )
    u_admin.rol = rol_admin

    user_details_service = UserDetailsService(usuario_repo)
    ud_cargado = user_details_service.load_user_by_email("dra.lucia@huellitas.com")
    assert ud_cargado.email == "dra.lucia@huellitas.com"
    assert ud_cargado.rol == "ADMIN"
    print("  ✓ UserDetailsService cargó usuario desde repositorio exitosamente")

    # -------------------------------------------------------------
    # 4. Pruebas de SecurityFilter (Extracción de Bearer Token)
    # -------------------------------------------------------------
    print("\n[4] Probando SecurityFilter...")

    filtro = SecurityFilter(jwt_service=jwt_service, user_details_service=user_details_service)

    # Token para Dra. Lucia
    token_lucia = jwt_service.generar_token("dra.lucia@huellitas.com", "ADMIN", "Dra. Lucia")
    header_auth = f"Bearer {token_lucia}"

    usuario_autenticado = filtro.autenticar(header_auth)
    assert usuario_autenticado is not None
    assert usuario_autenticado.email == "dra.lucia@huellitas.com"
    assert usuario_autenticado.es_admin() is True
    print(f"  ✓ SecurityFilter autenticó correctamente cabecera: {usuario_autenticado}")

    # Cabecera vacía o inválida
    assert filtro.autenticar(None) is None
    assert filtro.autenticar("Bearer token_invalido_xyz") is None
    print("  ✓ Cabeceras sin token o con token inválido devuelven None")

    # -------------------------------------------------------------
    # 5. Pruebas de SecurityConfig (Reglas de Acceso / Autorización)
    # -------------------------------------------------------------
    print("\n[5] Probando SecurityConfig y Control de Acceso...")

    # Regla: /api/auth/** es público (permitAll)
    SecurityConfig.validar_acceso("/api/auth/login", "POST", usuario=None)
    SecurityConfig.validar_acceso("/api/auth/registro", "POST", usuario=None)
    print("  ✓ Rutas /api/auth/** admiten acceso público sin credenciales")

    # Regla: Ruta privada sin login -> 401
    try:
        SecurityConfig.validar_acceso("/api/reservas", "POST", usuario=None)
        assert False
    except ApiException as e:
        assert e.status_code == 401
        assert e.mensaje == "Debes iniciar sesión para acceder a este recurso"
        print("  ✓ Acceso anónimo a ruta protegida bloqueado con HTTP 401")

    # Regla: Ruta admin con usuario cliente -> 403 Forbidden
    try:
        SecurityConfig.validar_acceso("/api/admin/usuarios", "GET", usuario=user_details_cli)
        assert False
    except ApiException as e:
        assert e.status_code == 403
        assert e.mensaje == "No tienes permisos para realizar esta acción"
        print("  ✓ Usuario CLIENTE bloqueado en /api/admin/** con HTTP 403 Forbidden")

    # Regla: Ruta admin con usuario admin -> Permitido
    SecurityConfig.validar_acceso("/api/admin/usuarios", "GET", usuario=user_details_admin)
    print("  ✓ Usuario ADMIN autorizado en /api/admin/**")

    # Regla: GET /api/servicios permitido para cliente y admin
    SecurityConfig.validar_acceso("/api/servicios", "GET", usuario=user_details_cli)
    SecurityConfig.validar_acceso("/api/servicios", "GET", usuario=user_details_admin)
    print("  ✓ GET /api/servicios autorizado para CLIENTE y ADMIN")

    # Regla: POST /api/servicios solo para admin
    try:
        SecurityConfig.validar_acceso("/api/servicios", "POST", usuario=user_details_cli)
        assert False
    except ApiException as e:
        assert e.status_code == 403
        print("  ✓ POST /api/servicios bloqueado para CLIENTE (403)")

    SecurityConfig.validar_acceso("/api/servicios", "POST", usuario=user_details_admin)
    print("  ✓ POST /api/servicios autorizado para ADMIN")

    # Regla: /api/reservas es exclusivo de CLIENTE (el admin no agenda ni cancela citas)
    SecurityConfig.validar_acceso("/api/reservas", "POST", usuario=user_details_cli)
    try:
        SecurityConfig.validar_acceso("/api/reservas", "POST", usuario=user_details_admin)
        assert False
    except ApiException as e:
        assert e.status_code == 403
        print("  ✓ /api/reservas restringido a CLIENTE (admin bloqueado con 403)")

    # -------------------------------------------------------------
    # 6. Pruebas de Decoradores de Seguridad
    # -------------------------------------------------------------
    print("\n[6] Probando Decoradores (@requerir_admin, @requerir_cliente)...")

    @requerir_admin
    def endpoint_solo_admin(usuario: UserDetails):
        return f"Bienvenido Admin {usuario.email}"

    @requerir_cliente
    def endpoint_solo_cliente(usuario: UserDetails):
        return f"Bienvenido Cliente {usuario.email}"

    assert endpoint_solo_admin(usuario=user_details_admin) == "Bienvenido Admin admin@huellitas.com"
    print("  ✓ @requerir_admin ejecutado por ADMIN con éxito")

    try:
        endpoint_solo_admin(usuario=user_details_cli)
        assert False
    except ApiException as e:
        assert e.status_code == 403
        print("  ✓ @requerir_admin bloqueó a CLIENTE con HTTP 403")

    assert endpoint_solo_cliente(usuario=user_details_cli) == "Bienvenido Cliente carlos@gmail.com"
    print("  ✓ @requerir_cliente ejecutado por CLIENTE con éxito")

    print("\n" + "=" * 70)
    print("¡TODAS LAS PRUEBAS DE CONFIG Y SECURITY PASARON EXITOSAMENTE!")
    print("=" * 70)


if __name__ == "__main__":
    probar_security_y_config()

