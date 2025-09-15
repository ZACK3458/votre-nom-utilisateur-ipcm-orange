"""Sécurité (offline) – Fournit une classe User minimale sans base de données.

Ce module évite toute dépendance à un ORM. Il reste compatible avec les tests
unitaires qui instancient directement ``User``.
"""

from dataclasses import dataclass


@dataclass
class User:
    """Utilisateur simple (offline).

    Champs:
        username: identifiant
        password: mot de passe (en clair ici, uniquement pour démonstration)
        role: rôle applicatif (ex: 'admin', 'user')
    """
    username: str
    password: str
    role: str = "user"

    # Hooks simples pour compat Flask-Login si utilisé indirectement
    @property
    def is_authenticated(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_active(self) -> bool:  # pragma: no cover
        return True

    @property
    def is_anonymous(self) -> bool:  # pragma: no cover
        return False

    def get_id(self) -> str:  # pragma: no cover
        return self.username

    def __repr__(self) -> str:
        return f"<User {self.username} ({self.role})>"
