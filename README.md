# votre-nom-utilisateur-ipcm-orange

Application IPCM (IP Capacity Management) 100% hors‑ligne, sans base de données, construite avec Flask pour Orange Cameroun. Tous les assets (Bootstrap, icônes, Chart.js) sont embarqués localement pour fonctionner sans Internet.

## Fonctionnalités clés
- Hors‑ligne par défaut: pas de base de données, données simulées côté serveur/cliente
- Authentification locale simplifiée (utilisateur hors‑ligne)
- Tableau de bord premium (KPI, donut santé, timeline d’alertes, trafic, dark mode persistant)
- Interfaces: recherche/filtre/tri/export CSV côté client, compteurs visible/total
- Reporting: export CSV, impression avec en‑tête/pied dédiés, mini‑graphique
- Prédictif: régression linéaire pure Python (aucune dépendance lourde)
- Architecture: topologie SVG interactive (couches L2/L3/MPLS)
- Accessibilité: attributs ARIA, gestion du clavier et états persistants

## Installation rapide
1. Cloner le dépôt
2. (Optionnel) Créer un venv et l’activer
3. Installer les dépendances: voir `requirements.txt`
4. Lancer l’application: `python run.py`

L’application sert les fichiers statiques locaux; aucune connexion réseau n’est requise à l’exécution.

## Tests
Exécuter la suite de tests unitaires:
- `python -m unittest discover -s tests -v`

## Documentation
- Cahier des charges et directives: `.github/copilot-instructions.md`
- Contexte et règles du projet: `.github/instructions/ORDRE.instructions.md`

## Licence
Projet interne Orange Cameroun. Usage selon les politiques internes.
