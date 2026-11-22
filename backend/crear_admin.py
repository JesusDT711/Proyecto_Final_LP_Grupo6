from getpass import getpass

from config.database import get_session_factory
from model.usuario import Usuario
from model.rol import Rol
from util.seguridad_util import SeguridadUtil

db = get_session_factory()()

try:
    email = input("Correo del administrador: ").strip().lower()
    nombre = input("Nombre completo: ").strip()
    password = getpass("Contraseña del administrador: ")

    if not email or not nombre:
        raise ValueError("El correo y el nombre son obligatorios.")

    if len(password) < 6:
        raise ValueError("La contraseña debe tener al menos 6 caracteres.")

    if len(password.encode("utf-8")) > 72:
        raise ValueError("La contraseña supera el límite permitido.")

    existente = db.query(Usuario).filter(
        Usuario.email == email
    ).first()

    if existente:
        raise ValueError("Ese correo ya está registrado. No se modificó su cuenta.")

    rol = db.query(Rol).filter(Rol.nombre == "ADMIN").first()

    if not rol:
        rol = Rol(nombre="ADMIN")
        db.add(rol)
        db.flush()

    admin = Usuario(
        email=email,
        nombre_completo=nombre,
        password=SeguridadUtil.encriptar_password(password),
        rol_id=rol.id
    )

    db.add(admin)
    db.commit()

    print("\n¡Cuenta ADMIN creada correctamente!")

except Exception as e:
    db.rollback()
    print(f"\nNo se pudo crear la cuenta: {e}")

finally:
    db.close()
