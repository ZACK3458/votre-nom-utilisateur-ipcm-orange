"""Collecte SNMP hors-ligne et tolérante aux dépendances.
Permet la collecte SNMP offline, avec fallback si pysnmp absent.
"""

try:
    from pysnmp.hlapi import (
        getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
    )
    _HAS_PYSNMP = True
except Exception:  # ImportError ou autre
    _HAS_PYSNMP = False


def collect_interface_data(ip, community, oid):
    """
    Collecte les données SNMP d'une interface réseau.

    Args:
        ip (str): Adresse IP cible.
        community (str): Communauté SNMP.
        oid (str): OID SNMP à interroger.

    Returns:
        dict | None: Résultat SNMP ou None si offline/fallback.
    """
    if not _HAS_PYSNMP:
        # Offline fallback
        return None
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    for (error_indication, error_status, error_index, var_binds) in iterator:
        if error_indication:
            return None
        elif error_status:
            return None
        else:
            return {str(name): str(val) for name, val in var_binds}
