"""
Module de gestion des erreurs et incidents : logging simple et handlers Flask.
Gère la journalisation des erreurs et les pages d'erreur personnalisées.
"""
from flask import render_template
from app import app


def log_error(error):
    """
    Journalise l'erreur (placeholder).
    Args:
        error (Exception): Exception à journaliser.
    """
    print(f'ERREUR: {error}')


@app.errorhandler(404)
def not_found(e):
    """
    Handler pour les erreurs 404 (page non trouvée).
    Args:
        e (Exception): Exception Flask.
    Returns:
        tuple: template et code 404.
    """
    log_error(e)
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    """
    Handler pour les erreurs 500 (erreur serveur).
    Args:
        e (Exception): Exception Flask.
    Returns:
        tuple: template et code 500.
    """
    log_error(e)
    return render_template('errors/500.html'), 500
