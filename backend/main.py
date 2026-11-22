"""Servidor HTTP (FastAPI) que expone los controllers del backend.
Ejecutar desde la carpeta backend:  uvicorn main:app --reload --port 8000"""
from contextlib import asynccontextmanager
from types import SimpleNamespace

from fastapi import Body, Depends, FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.database import get_db, get_session_factory, init_db
from config.settings import settings
from controller import (AuthController, MascotaController, ReservaAdminController,
                        ReservaController, ServicioController)
from exception.api_exception import ApiException
from model import Rol
from repository import (MascotaRepository, ReservaRepository, RolRepository,
                        ServicioRepository, UsuarioRepository)
from security.security_config import SecurityConfig
from security.security_filter import SecurityFilter
from security.user_details_service import UserDetailsService
from service import AuthService, MascotaService, ReservaService, ServicioService

# Servicios de ejemplo (solo se crean si la tabla está vacía). Edita nombres y precios a tu gusto.
SERVICIOS = [
    ("Consulta general", "Revisión completa de la salud de tu mascota.", 60, 30),
    ("Diagnóstico", "Análisis de laboratorio, rayos X y ecografías.", 120, 60),
    ("Odontología", "Limpieza y tratamiento dental para prevenir infecciones.", 90, 60),
    ("Endoscopía", "Exploración interna con mínima invasión.", 250, 60),
    ("Cirugía", "Procedimientos programados con seguimiento postoperatorio.", 350, 120),
    ("Oncología", "Diagnóstico y tratamiento especializado.", 200, 60),
]


@asynccontextmanager
async def lifespan(_):
    init_db()  # crea las tablas si no existen
    db = get_session_factory()()
    try:
        roles = RolRepository(db)
        for nombre in ("ADMIN", "CLIENTE"):
            if roles.buscar_por_nombre(nombre) is None:
                roles.guardar(Rol(nombre=nombre))
        svc = ServicioService(ServicioRepository(db))
        if not svc.listar_todos():
            for n, d, p, m in SERVICIOS:
                svc.crear(n, p, m, d)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])


@app.exception_handler(ApiException)
async def _api_error(_, e: ApiException):
    return JSONResponse(e.to_dict(), status_code=e.status_code)


@app.exception_handler(ValueError)
async def _valor_invalido(_, e: ValueError):
    return JSONResponse({"mensaje": "Datos inválidos", "status": 400}, status_code=400)


def ctx(request: Request, db=Depends(get_db)):
    """Arma repositorios, servicios y controllers sobre la sesión de la petición y valida el acceso."""
    roles, usuarios, mascotas = RolRepository(db), UsuarioRepository(db), MascotaRepository(db)
    servicios, reservas = ServicioRepository(db), ReservaRepository(db)
    usuario = SecurityFilter(user_details_service=UserDetailsService(usuarios)).autenticar(request.headers.get("Authorization"))
    # El README indica que listar servicios es público (la validación original pediría sesión)
    if not (request.method == "GET" and request.url.path.startswith("/api/servicios")):
        SecurityConfig.validar_acceso(request.url.path, request.method, usuario)
    rs = ReservaService(reservas, servicios, usuarios, mascotas)
    return SimpleNamespace(
        email=usuario.email if usuario else None,
        auth=AuthController(AuthService(usuarios, roles)),
        servicio=ServicioController(ServicioService(servicios)),
        mascota=MascotaController(MascotaService(mascotas, usuarios, reservas)),
        reserva=ReservaController(rs),
        admin=ReservaAdminController(rs),
    )


def out(r):
    """Convierte la ApiResponse del controller en respuesta JSON."""
    d = r.data
    d = [x.to_dict() for x in d] if isinstance(d, list) else d.to_dict() if d is not None else None
    return JSONResponse(jsonable_encoder(d), status_code=r.status_code)


# ---- Auth ----
@app.post("/api/auth/registro")
def registro(datos: dict = Body(...), c=Depends(ctx)): return out(c.auth.registrar(datos))

@app.post("/api/auth/login")
def login(datos: dict = Body(...), c=Depends(ctx)): return out(c.auth.login(datos))

# ---- Servicios ----
@app.get("/api/servicios")
def servicios(c=Depends(ctx)): return out(c.servicio.listar())

@app.get("/api/servicios/buscar")
def buscar(nombre: str = "", c=Depends(ctx)): return out(c.servicio.buscar(nombre))

@app.get("/api/servicios/{id}")
def servicio(id: int, c=Depends(ctx)): return out(c.servicio.obtener(id))

@app.post("/api/servicios")
def crear_servicio(datos: dict = Body(...), c=Depends(ctx)): return out(c.servicio.crear(datos))

@app.put("/api/servicios/{id}")
def editar_servicio(id: int, datos: dict = Body(...), c=Depends(ctx)): return out(c.servicio.actualizar(id, datos))

@app.delete("/api/servicios/{id}")
def borrar_servicio(id: int, c=Depends(ctx)): return out(c.servicio.eliminar(id))

# ---- Reservas (CLIENTE) ----
@app.post("/api/reservas")
def reservar(datos: dict = Body(...), c=Depends(ctx)): return out(c.reserva.crear(datos, c.email))

@app.get("/api/reservas/mis-reservas")
def mis_reservas(c=Depends(ctx)): return out(c.reserva.mis_reservas(c.email))

@app.put("/api/reservas/{id}/cancelar")
def cancelar(id: int, c=Depends(ctx)): return out(c.reserva.cancelar(id, c.email))

# ---- Reservas (ADMIN) ----
@app.get("/api/admin/reservas")
def todas_reservas(estado: str = None, c=Depends(ctx)): return out(c.admin.listar(estado))

@app.put("/api/admin/reservas/{id}/atendida")
def atendida(id: int, c=Depends(ctx)): return out(c.admin.marcar_atendida(id))

# ---- Mascotas ----
@app.post("/api/mascotas")
def registrar_mascota(datos: dict = Body(...), c=Depends(ctx)): return out(c.mascota.registrar(datos, c.email))

@app.get("/api/mascotas/mis-mascotas")
def mis_mascotas(c=Depends(ctx)): return out(c.mascota.mis_mascotas(c.email))