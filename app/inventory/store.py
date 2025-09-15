"""Stockage hors-ligne de l'inventaire via un fichier JSON.

Pas de base de données. Persistance simple avec support des modèles Equipment complets.
"""
from __future__ import annotations

import json
import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from .models import Equipment, NetworkDomain, EquipmentType, SupportStatus

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
# Allow override via env var for tests or custom location
INVENTORY_PATH = os.environ.get('IPCM_INVENTORY_PATH') or os.path.join(DATA_DIR, 'inventory.json')
INTERFACES_HISTORY_PATH = os.environ.get('IPCM_INTERFACES_HISTORY_PATH') or os.path.join(DATA_DIR, 'interfaces_history.json')


def _ensure_store() -> None:
    """Assure l'existence des fichiers de stockage."""
    os.makedirs(DATA_DIR, exist_ok=True)
    # Ensure parent dir of inventory path exists
    os.makedirs(os.path.dirname(INVENTORY_PATH), exist_ok=True)
    if not os.path.exists(INVENTORY_PATH):
        # Créer avec des données d'exemple
        sample_data = _create_sample_inventory()
        with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump(sample_data, f, ensure_ascii=False, indent=2)
    
    # Initialize interfaces history file
    if not os.path.exists(INTERFACES_HISTORY_PATH):
        with open(INTERFACES_HISTORY_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)


def _create_sample_inventory() -> List[Dict[str, Any]]:
    """Crée des données d'exemple pour l'inventaire IPCM."""
    now = datetime.now()
    
    # Routeur principal Backbone
    router_backbone = Equipment(
        id=1,
        name="RTR-BBN-01",
        type=EquipmentType.ROUTER,
        brand="Cisco",
        model="ASR9000",
        software_version="IOS-XR 7.8.1",
        ip_address="192.168.100.1",
        location="Douala - Site Principal",
        domain=NetworkDomain.BACKBONE,
        support_status=SupportStatus.ACTIVE,
        modules=["RSP-8G", "4x10GE-DWDM", "2x100GE"],
        snmp_enabled=True,
        serial_number="FXS2142L0A1",
        asset_tag="BB-RTR-001",
        criticality_level="critical",
        installation_date=datetime(2020, 3, 15),
        vendor_support_contract="Premium 24/7"
    )
    
    # Switch Datacenter
    switch_dc = Equipment(
        id=2,
        name="SW-DC-CORE-01",
        type=EquipmentType.SWITCH,
        brand="Juniper",
        model="EX9200",
        software_version="Junos 21.4R1",
        ip_address="192.168.100.10",
        location="Yaoundé - Datacenter",
        domain=NetworkDomain.DATACENTER,
        support_status=SupportStatus.ACTIVE,
        modules=["48x10GE", "4x40GE", "Redundant PSU"],
        snmp_enabled=True,
        serial_number="JN118AF2100",
        asset_tag="DC-SW-001",
        criticality_level="high",
        installation_date=datetime(2021, 1, 10),
        vendor_support_contract="Standard Support"
    )
    
    # Routeur LAN d'accès
    router_lan = Equipment(
        id=3,
        name="RTR-LAN-ACCESS-01",
        type=EquipmentType.ROUTER,
        brand="Cisco",
        model="ISR4331",
        software_version="IOS 16.12.04",
        ip_address="192.168.50.1",
        location="Douala - Bâtiment A",
        domain=NetworkDomain.LAN,
        support_status=SupportStatus.ACTIVE,
        modules=["4x1GE", "2xSFP+", "Security Module"],
        snmp_enabled=True,
        serial_number="FDO24120JX8",
        asset_tag="LAN-RTR-001",
        criticality_level="medium",
        installation_date=datetime(2022, 6, 20),
        vendor_support_contract="Basic Support"
    )
    
    return [
        router_backbone.to_dict(),
        switch_dc.to_dict(),
        router_lan.to_dict()
    ]


def load_inventory() -> List[Dict[str, Any]]:
    """Charge l'inventaire depuis le fichier JSON."""
    _ensure_store()
    with open(INVENTORY_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_equipment_objects() -> List[Equipment]:
    """Charge l'inventaire et retourne une liste d'objets Equipment."""
    data = load_inventory()
    return [Equipment.from_dict(item) for item in data]


def save_inventory(items: List[Dict[str, Any]]) -> None:
    """Sauvegarde l'inventaire dans le fichier JSON."""
    _ensure_store()
    with open(INVENTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def save_equipment_objects(equipments: List[Equipment]) -> None:
    """Sauvegarde une liste d'objets Equipment."""
    data = [eq.to_dict() for eq in equipments]
    save_inventory(data)


def _next_id(items: List[Dict[str, Any]]) -> int:
    """Génère le prochain ID disponible."""
    return (max([it.get('id', 0) for it in items]) + 1) if items else 1


def add_equipment(data: Dict[str, Any]) -> Dict[str, Any]:
    """Ajoute un nouvel équipement."""
    items = load_inventory()
    
    # Créer l'objet Equipment avec les données fournies
    eq_data = {**data}
    eq_data['id'] = _next_id(items)
    
    # Si les types sont des strings, on les convertit
    if 'type' in eq_data and isinstance(eq_data['type'], str):
        try:
            eq_data['type'] = EquipmentType(eq_data['type'])
        except ValueError:
            eq_data['type'] = EquipmentType.OTHER
    
    if 'domain' in eq_data and isinstance(eq_data['domain'], str):
        try:
            eq_data['domain'] = NetworkDomain(eq_data['domain'])
        except ValueError:
            eq_data['domain'] = NetworkDomain.LAN
    
    if 'support_status' in eq_data and isinstance(eq_data['support_status'], str):
        try:
            eq_data['support_status'] = SupportStatus(eq_data['support_status'])
        except ValueError:
            eq_data['support_status'] = SupportStatus.ACTIVE
    
    # Créer l'objet Equipment et le convertir en dict
    equipment = Equipment(**eq_data)
    eq_dict = equipment.to_dict()
    
    items.append(eq_dict)
    save_inventory(items)
    return eq_dict


def update_equipment(equip_id: int, changes: Dict[str, Any]) -> bool:
    """Met à jour un équipement existant."""
    items = load_inventory()
    found = False
    
    for item in items:
        if item.get('id') == equip_id:
            # Convertir en objet Equipment pour validation
            equipment = Equipment.from_dict(item)
            
            # Appliquer les changements
            for key, value in changes.items():
                if hasattr(equipment, key):
                    setattr(equipment, key, value)
            
            # Mettre à jour la date de modification
            equipment.updated_at = datetime.now()
            
            # Reconvertir en dict et remplacer dans la liste
            items[items.index(item)] = equipment.to_dict()
            found = True
            break
    
    if found:
        save_inventory(items)
    return found


def delete_equipment(equip_id: int) -> bool:
    """Supprime un équipement."""
    items = load_inventory()
    new_items = [it for it in items if it.get('id') != equip_id]
    if len(new_items) != len(items):
        save_inventory(new_items)
        return True
    return False


def get_equipment_by_id(equip_id: int) -> Optional[Equipment]:
    """Récupère un équipement par son ID."""
    items = load_inventory()
    for item in items:
        if item.get('id') == equip_id:
            return Equipment.from_dict(item)
    return None


def get_equipments_by_domain(domain: NetworkDomain) -> List[Equipment]:
    """Récupère tous les équipements d'un domaine donné."""
    equipments = load_equipment_objects()
    return [eq for eq in equipments if eq.domain == domain]


def get_equipments_by_type(equipment_type: EquipmentType) -> List[Equipment]:
    """Récupère tous les équipements d'un type donné."""
    equipments = load_equipment_objects()
    return [eq for eq in equipments if eq.type == equipment_type]


def get_critical_equipments() -> List[Equipment]:
    """Récupère les équipements critiques."""
    equipments = load_equipment_objects()
    return [eq for eq in equipments if eq.criticality_level == "critical"]


def save_interface_history(equipment_id: int, interface_data: Dict[str, Any]) -> None:
    """Sauvegarde l'historique des données d'interface pour l'analyse prédictive."""
    _ensure_store()
    
    try:
        with open(INTERFACES_HISTORY_PATH, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
    
    history_entry = {
        'equipment_id': equipment_id,
        'timestamp': datetime.now().isoformat(),
        'interface_data': interface_data
    }
    
    history.append(history_entry)
    
    # Garder seulement les 10000 dernières entrées pour éviter un fichier trop volumineux
    if len(history) > 10000:
        history = history[-10000:]
    
    with open(INTERFACES_HISTORY_PATH, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


def load_interface_history(equipment_id: Optional[int] = None, days: int = 30) -> List[Dict[str, Any]]:
    """Charge l'historique des interfaces, optionnellement filtré par équipement et période."""
    try:
        with open(INTERFACES_HISTORY_PATH, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []
    
    # Filtrer par équipement si spécifié
    if equipment_id is not None:
        history = [entry for entry in history if entry.get('equipment_id') == equipment_id]
    
    # Filtrer par période (derniers X jours)
    if days > 0:
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        history = [
            entry for entry in history 
            if datetime.fromisoformat(entry['timestamp']).timestamp() >= cutoff_date
        ]
    
    return history
