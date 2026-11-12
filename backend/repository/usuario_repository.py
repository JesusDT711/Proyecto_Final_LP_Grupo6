
from typing import Any, List, Optional
try:
    from model.usuario import Usuario
    from util.email_util import EmailUtil
except ImportError:
    from backend.model.usuario import Usuario
    from backend.util.email_util import EmailUtil
from .base_repository import BaseRepository


class UsuarioRepository(BaseRepository[Usuario]):

    def __init__(self, session: Optional[Any] = None):
        super().__init__(Usuario, session)

    def buscar_por_email(self, email: str) -> Optional[Usuario]:

        email_clean = EmailUtil.normalizar(email)
        if not email_clean:
            return None

        if self.session is not None:
            return self.session.query(Usuario).filter(Usuario.email == email_clean).first()

        for u in self._memoria.values():
            if EmailUtil.normalizar(u.email) == email_clean:
                return u
        return None

    def existe_por_email(self, email: str) -> bool:

        email_clean = EmailUtil.normalizar(email)
        if not email_clean:
            return False

        if self.session is not None:
            return self.session.query(Usuario.id).filter(Usuario.email == email_clean).first() is not None

        return any(EmailUtil.normalizar(u.email) == email_clean for u in self._memoria.values())

    def existe_por_email_y_distinto_id(self, email: str, id: int) -> bool:
    
        email_clean = EmailUtil.normalizar(email)
        if not email_clean:
            return False

        if self.session is not None:
            return (
                self.session.query(Usuario.id)
                .filter(Usuario.email == email_clean, Usuario.id != id)
                .first()
                is not None
            )

        return any(
            EmailUtil.normalizar(u.email) == email_clean and u.id != id
            for u in self._memoria.values()
        )
