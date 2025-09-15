"""Collecte SNMP hors-ligne et tolérante aux dépendances.

Si pysnmp n'est pas disponible, la fonction retourne None afin de rester
compatible avec l'exécution offline et les tests unitaires.
"""

try:
    from pysnmp.hlapi import (
        getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity
    )
    _HAS_PYSNMP = True
except Exception:  # ImportError ou autre
    _HAS_PYSNMP = False


def collect_interface_data(ip, community, oid):
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
    for (errorIndication, errorStatus, errorIndex, varBinds) in iterator:
        if errorIndication:
            return None
        elif errorStatus:
            return None
        else:
            return {str(name): str(val) for name, val in varBinds}
