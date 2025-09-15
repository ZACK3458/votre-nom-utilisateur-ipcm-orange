"""Stockage hors-ligne de l'inventaire via un fichier JSON.

Pas de base de données. Persistance simple dans c:/orange/data/inventory.json
"""
from __future__ import annotations

import json
import os
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
# Allow override via env var for tests or custom location
INVENTORY_PATH = os.environ.get('IPCM_INVENTORY_PATH') or os.path.join(DATA_DIR, 'inventory.json')


def _ensure_store() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    # Ensure parent dir of inventory path exists
    os.makedirs(os.path.dirname(INVENTORY_PATH), exist_ok=True)
    if not os.path.exists(INVENTORY_PATH):
        with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def load_inventory() -> List[Dict[str, Any]]:
    _ensure_store()
    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_inventory(items: List[Dict[str, Any]]) -> None:
    _ensure_store()
    with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def _next_id(items: List[Dict[str, Any]]) -> int:
    return (max([it.get('id', 0) for it in items]) + 1) if items else 1


def add_equipment(data: Dict[str, Any]) -> Dict[str, Any]:
    items = load_inventory()
    eq = {**data}
    eq['id'] = _next_id(items)
    items.append(eq)
    save_inventory(items)
    return eq


def update_equipment(equip_id: int, changes: Dict[str, Any]) -> bool:
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
    items = load_inventory()
    new_items = [it for it in items if it.get('id') != equip_id]
    if len(new_items) != len(items):
        save_inventory(new_items)
        return True
    return False
