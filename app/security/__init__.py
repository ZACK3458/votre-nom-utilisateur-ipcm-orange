"""Package security (offline).

Expose une classe `User` minimale afin que `from app.security import User`
fonctionne sans base de données ni ORM.
Ce module gère la sécurité offline, les rôles et l'authentification simplifiée.
"""

from dataclasses import dataclass


@dataclass
class User:
    """Utilisateur offline minimal pour IPCM Orange Cameroun.
    Attributs : username, password, role (par défaut 'user').
    """

    username: str
    password: str
    role: str = "user"

    @property
    def is_authenticated(self) -> bool:  # pragma: no cover
        """Retourne True si l'utilisateur est authentifié (offline toujours True)."""
        return True

    @property
    def is_active(self) -> bool:  # pragma: no cover
        """Retourne True si l'utilisateur est actif (offline toujours True)."""
        return True

    @property
    def is_anonymous(self) -> bool:  # pragma: no cover
        """Retourne False car l'utilisateur offline n'est jamais anonyme."""
        return False

    def get_id(self) -> str:  # pragma: no cover
        """Retourne l'identifiant unique de l'utilisateur (username)."""
        return self.username
