from config.database import get_session_factory
from model.usuario import Usuario

db = get_session_factory()()

try:
    usuarios = db.query(Usuario).all()

    print("\n--- USUARIOS REGISTRADOS ---")

    for usuario in usuarios:
        rol = usuario.rol.nombre if usuario.rol else "Sin rol"
        print(f"Correo: {usuario.email} | Rol: {rol}")

finally:
    db.close()
