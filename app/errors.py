"""
Module de gestion des erreurs et incidents: logging simple et handlers Flask.
"""
from flask import render_template
from app import app


def log_error(error):
    """Journalise l'erreur (placeholder)."""
    print(f'ERREUR: {error}')


@app.errorhandler(404)
def not_found(e):
    log_error(e)
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    log_error(e)
    return render_template('errors/500.html'), 500
