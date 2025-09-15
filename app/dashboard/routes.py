"""Blueprint Dashboard (offline, sans base de données).
Fournit la route /dashboard via un blueprint, utilisant des données simulées pour IPCM Orange Cameroun.
"""
from flask import Blueprint, render_template

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
def dashboard():
    """
    Affiche le dashboard principal avec équipements, utilisateurs et interfaces simulés.
    Returns:
        template dashboard.html avec données simulées.
    """
    equipments = [
        {'name': 'Router01', 'type': 'Routeur', 'ip_address': '192.168.1.1'},
        {'name': 'Switch02', 'type': 'Switch', 'ip_address': '192.168.1.2'},
        {'name': 'Firewall03', 'type': 'Firewall', 'ip_address': '192.168.1.3'},
    ]
    users = [
        {'username': 'admin', 'role': 'Administrateur'},
        {'username': 'user1', 'role': 'Utilisateur principal'},
    ]
    interfaces = [
        {'name': 'Gig0/1', 'status': 'active'},
        {'name': 'Gig0/2', 'status': 'inactive'},
        {'name': 'Eth1/1', 'status': 'active'},
    ]
    return render_template('dashboard.html', equipments=equipments, users=users, interfaces=interfaces)
