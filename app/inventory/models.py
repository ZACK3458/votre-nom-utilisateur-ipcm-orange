"""Modèles d'inventaire hors-ligne (sans base de données).

Ce module fournit une simple dataclass Equipment pour représenter un
équipement réseau. Aucune dépendance à SQLAlchemy ni à un objet `db`.
"""

from dataclasses import dataclass


@dataclass
class Equipment:
    id: int | None = None
    name: str = ""
    type: str = ""
    brand: str = ""
    model: str = ""
    software_version: str = ""
    ip_address: str = ""
    location: str = ""
    support_status: str = ""
    modules: str = ""

    def __repr__(self) -> str:
        return f"<Equipment {self.name} ({self.type})>"
