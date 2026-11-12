
import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent
repo_dir = backend_dir.parent
for p in [str(repo_dir), str(backend_dir)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from datetime import date, datetime
from decimal import Decimal

try:
    from model import (
        Base,
        EstadoReserva,
        Rol,
        Usuario,
        Mascota,
        Servicio,
        Reserva,
        Atencion,
        SQLALCHEMY_INSTALLED,
    )
except ImportError:
    from backend.model import (
        Base,
        EstadoReserva,
        Rol,
        Usuario,
        Mascota,
        Servicio,
        Reserva,
        Atencion,
        SQLALCHEMY_INSTALLED,
    )



def ejecutar_pruebas():
    print("=" * 60)
    print("VERIFICACIÓN DE MODELOS DEL BACKEND - VETERINARIA HUELLITAS")
    print(f"SQLAlchemy disponible en entorno: {SQLALCHEMY_INSTALLED}")
    print("=" * 60)

    # 1. Probar Rol
    rol_admin = Rol(id=1, nombre="ADMIN")
    rol_cliente = Rol(id=2, nombre="CLIENTE")
    print("\n[OK] Rol creado:")
    print(" ", repr(rol_admin))
    print("  to_dict():", rol_admin.to_dict())

    # 2. Probar Usuario
    usuario_cliente = Usuario(
        id=1,
        email="carlos@example.com",
        password="hashed_password_123",
        nombre_completo="Carlos Rodriguez",
        telefono="987654321",
        rol_id=rol_cliente.id,
        created_at=datetime.now(),
    )
    usuario_cliente.rol = rol_cliente

    usuario_vet = Usuario(
        id=2,
        email="vet_ana@huellitas.com",
        password="hashed_password_456",
        nombre_completo="Dra. Ana Lopez",
        telefono="912345678",
        rol_id=rol_admin.id,
        created_at=datetime.now(),
    )
    usuario_vet.rol = rol_admin

    print("\n[OK] Usuarios creados:")
    print(" ", repr(usuario_cliente))
    print("  to_dict (sin pass):", usuario_cliente.to_dict())
    print("  to_dict (con pass):", usuario_cliente.to_dict(include_sensitive=True))

    # 3. Probar Mascota
    mascota = Mascota(
        id=10,
        nombre="Firulais",
        especie="Canino",
        raza="Golden Retriever",
        sexo="Macho",
        fecha_nacimiento=date(2021, 5, 14),
        usuario_id=usuario_cliente.id,
        created_at=datetime.now(),
    )
    mascota.usuario = usuario_cliente
    print("\n[OK] Mascota creada:")
    print(" ", repr(mascota))
    print("  to_dict():", mascota.to_dict())

    # 4. Probar Servicio
    servicio = Servicio(
        id=100,
        nombre="Consulta Veterinaria General",
        descripcion="Revisión médica completa, control de peso y signos vitales.",
        precio=Decimal("50.00"),
        duracion_minutos=30,
        activo=True,
        created_at=datetime.now(),
    )
    print("\n[OK] Servicio creado:")
    print(" ", repr(servicio))
    print("  to_dict():", servicio.to_dict())

    # 5. Probar Reserva
    fecha_inicio = datetime(2026, 11, 20, 10, 0, 0)
    fecha_fin = datetime(2026, 11, 20, 10, 30, 0)
    reserva = Reserva(
        id=1000,
        fecha_hora=fecha_inicio,
        fecha_hora_fin=fecha_fin,
        mascota_id=mascota.id,
        usuario_id=usuario_cliente.id,
        servicio_id=servicio.id,
        observaciones="Control de vacunas y desparasitación anual",
        estado=EstadoReserva.CONFIRMADA,
        creada_en=datetime.now(),
    )
    reserva.mascota = mascota
    reserva.usuario = usuario_cliente
    reserva.servicio = servicio

    print("\n[OK] Reserva creada:")
    print(" ", repr(reserva))
    print("  to_dict():", reserva.to_dict())

    # 6. Probar Atencion (Expediente médico)
    atencion = Atencion(
        id=5000,
        reserva_id=reserva.id,
        peso_kg=Decimal("28.50"),
        diagnostico_o_detalle="Paciente en buen estado general, pelaje sano y temperatura normal.",
        tratamiento_o_indicaciones="Se administra vacuna antirrábica y refuerzo séxtuple.",
        fecha_atencion=datetime.now(),
        atendido_por_id=usuario_vet.id,
    )
    atencion.reserva = reserva
    atencion.atendido_por = usuario_vet
    reserva.atencion = atencion

    print("\n[OK] Atencion (Expediente médico) creada:")
    print(" ", repr(atencion))
    print("  to_dict():", atencion.to_dict())

    print("\n" + "=" * 60)
    print("TODOS LOS MODELOS FUERON VALIDADOS EXITOSAMENTE")
    print("=" * 60)


if __name__ == "__main__":
    ejecutar_pruebas()

