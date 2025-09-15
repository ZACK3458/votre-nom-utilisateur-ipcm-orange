"""
Module d'analyse prédictive de capacité (offline, sans dépendances lourdes)

Fourni une régression linéaire simple sur les points historiques pour estimer
les périodes futures. Entrée: liste de tuples (date, valeur).
Sortie: liste de valeurs prédites (float) de longueur `periods`.
"""

from typing import Iterable, List, Tuple


def _linear_regression_coeffs(y: Iterable[float]) -> Tuple[float, float]:
    """Calcule les coefficients (pente m, ordonnée b) via moindres carrés.

    Utilise x = 0..n-1 pour les abscisses. Gère les cas dégénérés (n<2).
    """
    y_list = list(float(v) for v in y)
    n = len(y_list)
    if n < 2:
        # Pas assez de points pour une pente: retourne moyenne et pente nulle
        mean = y_list[0] if n == 1 else 0.0
        return 0.0, mean

    sum_x = (n - 1) * n / 2.0
    sum_x2 = (n - 1) * n * (2 * n - 1) / 6.0
    sum_y = sum(y_list)
    sum_xy = sum(i * v for i, v in enumerate(y_list))

    denom = n * sum_x2 - sum_x * sum_x
    if denom == 0:
        # Tous x identiques (ne devrait pas arriver ici) -> pente nulle
        m = 0.0
    else:
        m = (n * sum_xy - sum_x * sum_y) / denom
    b = (sum_y - m * sum_x) / n
    return m, b


def predict_capacity(data: List[Tuple[str, float]], periods: int = 12) -> List[float] | None:
    """Prédit `periods` points futurs par régression linéaire simple.

    data: liste de tuples (date, valeur)
    periods: nombre de pas à prédire
    """
    if not data:
        # Pour rester compatible avec le test unitaire actuel, retourner None
        return None

    # On n'utilise pas la date dans ce modèle simple; on respecte seulement l'ordre
    y_series = [float(v) for _, v in data]
    m, b = _linear_regression_coeffs(y_series)

    n = len(y_series)
    preds = [m * (n + i) + b for i in range(periods)]
    return preds
