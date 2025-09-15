
from flask import render_template, redirect, url_for, send_from_directory, jsonify
import time
from app import app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/users')
def users():
    return render_template('user_space/user_space.html')

@app.route('/inventory')
def inventory():
    return render_template('roadmap/roadmap.html')

@app.route('/snmp')
def snmp():
    return render_template('interfaces/interfaces.html')

@app.route('/dashboard')
def dashboard():
    # Données simulées pour le frontend IPCM
    equipments = [
        {'name': 'Router01', 'type': 'Routeur', 'ip_address': '192.168.1.1'},
        {'name': 'Switch02', 'type': 'Switch', 'ip_address': '192.168.1.2'},
        {'name': 'Firewall03', 'type': 'Firewall', 'ip_address': '192.168.1.3'}
    ]
    users = [
        {'username': 'admin', 'role': 'Administrateur'},
        {'username': 'user1', 'role': 'Utilisateur principal'}
    ]
    interfaces = [
        {'name': 'Gig0/1', 'status': 'active'},
        {'name': 'Gig0/2', 'status': 'inactive'},
        {'name': 'Eth1/1', 'status': 'active'}
    ]
    return render_template('dashboard.html', equipments=equipments, users=users, interfaces=interfaces)

@app.route('/reporting')
def reporting():
    return render_template('reporting.html')

@app.route('/predictive')
def predictive():
    return render_template('predictive.html')

@app.route('/security')
def security():
    return render_template('security.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/roadmap')
def roadmap():
    return render_template('roadmap/roadmap.html')

@app.route('/interfaces')
def interfaces():
    return render_template('interfaces/interfaces.html')

@app.route('/user-space')
def user_space():
    return render_template('user_space/user_space.html')

@app.route('/service')
def service():
    return render_template('service/service.html')

@app.route('/admin-data')
def admin_data():
    return render_template('admin-data.html')

@app.route('/plan-adressage')
def plan_adressage():
    return render_template('plan-adressage.html')

@app.route('/architecture')
def architecture():
    return render_template('architecture.html')

@app.route('/healthz')
def healthz():
    """Endpoint de santé simple pour les probes/monitoring.
    Retourne un JSON minimal indiquant le bon fonctionnement.
    """
    return jsonify(status='ok'), 200

@app.route('/metrics')
def metrics():
    """Expose des métriques basiques pour supervision/light observability."""
    uptime = time.time() - getattr(app, 'start_time', time.time())
    routes_count = len(app.url_map._rules)
    return jsonify({
        'service': app.config.get('SERVICE_NAME', 'ipcm'),
        'version': app.config.get('VERSION', '0.0.0'),
        'uptime_s': round(uptime, 3),
        'routes_count': routes_count,
        'status': 'ok'
    }), 200

# Extra routes referenced by navbar
@app.route('/precablage')
def precablage():
    # Placeholder page mapped to existing service template
    return render_template('service/service.html')

@app.route('/journal')
def journal():
    # Placeholder: reuse reporting layout for activity journal
    return render_template('reporting.html')

@app.route('/logout')
def logout():
    # Offline mode: just redirect to dashboard
    return redirect(url_for('index'))

@app.route('/')
def index():
    # Données simulées pour le frontend IPCM
    equipments = [
        {'name': 'Router01', 'type': 'Routeur', 'ip_address': '192.168.1.1'},
        {'name': 'Switch02', 'type': 'Switch', 'ip_address': '192.168.1.2'},
        {'name': 'Firewall03', 'type': 'Firewall', 'ip_address': '192.168.1.3'}
    ]
    users = [
        {'username': 'admin', 'role': 'Administrateur'},
        {'username': 'user1', 'role': 'Utilisateur principal'}
    ]
    interfaces = [
        {'name': 'Gig0/1', 'status': 'active'},
        {'name': 'Gig0/2', 'status': 'inactive'},
        {'name': 'Eth1/1', 'status': 'active'}
    ]
    return render_template('dashboard.html', equipments=equipments, users=users, interfaces=interfaces)
