"""
Stockage hors-ligne de l'inventaire via un fichier JSON.
Pas de base de données. Persistance simple dans c:/orange/data/inventory.json
Ce module fournit les fonctions CRUD pour l'inventaire offline.
"""
from __future__ import annotations

import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
# Permet la surcharge via variable d'environnement pour les tests ou custom
INVENTORY_PATH = os.environ.get('IPCM_INVENTORY_PATH') or os.path.join(DATA_DIR, 'inventory.json')


def _ensure_store() -> None:
    """Crée le dossier et le fichier inventaire si absent."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(INVENTORY_PATH), exist_ok=True)
    if not os.path.exists(INVENTORY_PATH):
        with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_inventory() -> List[Dict[str, Any]]:
    """Charge l'inventaire depuis le fichier JSON local."""
    _ensure_store()
    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_inventory(items: List[Dict[str, Any]]) -> None:
    """Sauvegarde la liste d'équipements dans le fichier JSON local."""
    _ensure_store()
    with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def _next_id(items: List[Dict[str, Any]]) -> int:
    """Retourne le prochain ID disponible pour un nouvel équipement."""
    return (max([it.get('id', 0) for it in items]) + 1) if items else 1


def add_equipment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ajoute un nouvel équipement à l'inventaire."""
    items = load_inventory()
    eq = {**data}
    eq['id'] = _next_id(items)
    items.append(eq)
    save_inventory(items)
    return eq


def update_equipment(equip_id: int, changes: Dict[str, Any]) -> bool:
    """Met à jour un équipement existant par son ID."""
    items = load_inventory()
    found = False
    for it in items:
        if it.get('id') == equip_id:
            it.update(changes)
            found = True
            break
    if found:
        save_inventory(items)
    return found


def delete_equipment(equip_id: int) -> bool:
    """Supprime un équipement de l'inventaire par son ID."""
    """Supprime un équipement de l'inventaire par son ID."""
    current_items = load_inventory()
    new_items = [it for it in current_items if it.get('id') != equip_id]
    if len(new_items) != len(current_items):
        save_inventory(new_items)
        return True
    return False
