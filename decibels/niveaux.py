"""Calculs sur des niveaux sonores exprimés en décibels.

Définitions appliquées (chantier/CONTRAT.md, rubrique « Ce que la bibliothèque fera », et
définitions de la consigne de la tâche B) :

- somme énergétique :    L = 10·log10(Σ 10^(Li/10))
- moyenne énergétique :  L = 10·log10((1/n)·Σ 10^(Li/10))
- moyenne arithmétique : L = (1/n)·Σ Li

Les Li sont des niveaux en décibels, de même nature et de même référence ; n est leur nombre.

Chaque fonction prend un itérable de niveaux, qu'elle parcourt une seule fois, et rend un
flottant. Les niveaux négatifs sont des valeurs comme les autres. Sont refusés :

- un itérable vide : `ValueError` ;
- une valeur qui n'est ni `int` ni `float`, ou un booléen : `TypeError` ;
- une valeur infinie ou indéfinie (NaN) : `ValueError`.
"""

import math
from collections.abc import Iterable
from fractions import Fraction

__all__ = ["moyenne_arithmetique", "moyenne_energetique", "somme_niveaux"]


def somme_niveaux(niveaux: Iterable[float]) -> float:
    """Rend la somme énergétique des niveaux : L = 10·log10(Σ 10^(Li/10)).

    C'est le niveau obtenu en additionnant les énergies, par exemple celui de plusieurs sources
    sonores indépendantes : deux sources de 60 dB donnent 63,01 dB.

    Lève `ValueError` si `niveaux` est vide ou contient une valeur infinie ou NaN, et `TypeError`
    si une valeur n'est ni `int` ni `float` ou si c'est un booléen.
    """
    valeurs = _valider_niveaux(niveaux)
    return _niveau_des_energies(valeurs, 1)


def moyenne_energetique(niveaux: Iterable[float]) -> float:
    """Rend la moyenne énergétique des niveaux : L = 10·log10((1/n)·Σ 10^(Li/10)).

    C'est la moyenne d'usage en acoustique : celle des énergies, ramenée en décibels. Des niveaux
    de 60 dB et 70 dB donnent 67,40 dB. Elle n'est jamais inférieure à la moyenne arithmétique
    des mêmes niveaux, et lui est égale quand ils sont tous égaux.

    Lève `ValueError` si `niveaux` est vide ou contient une valeur infinie ou NaN, et `TypeError`
    si une valeur n'est ni `int` ni `float` ou si c'est un booléen.
    """
    valeurs = _valider_niveaux(niveaux)
    moyenne = _niveau_des_energies(valeurs, len(valeurs))
    # La moyenne énergétique n'est jamais inférieure à la moyenne arithmétique : le logarithme
    # d'une moyenne vaut au moins la moyenne des logarithmes (inégalité de Jensen). Quand les
    # niveaux sont presque égaux, les arrondis du calcul ci-dessus peuvent pourtant la placer un
    # cran en dessous. La moyenne arithmétique, arrondie correctement, sert alors de plancher :
    # le résultat ne peut qu'y gagner en justesse.
    return max(moyenne, _moyenne_exacte(valeurs))


def moyenne_arithmetique(niveaux: Iterable[float]) -> float:
    """Rend la moyenne arithmétique des niveaux : L = (1/n)·Σ Li.

    Simple moyenne des valeurs en décibels, sans passer par les énergies : 60 dB et 70 dB donnent
    65 dB. Ce n'est pas la moyenne d'usage en acoustique (voir `moyenne_energetique`) ; elle est
    fournie à part parce que certaines méthodes de mesure la demandent.

    Lève `ValueError` si `niveaux` est vide ou contient une valeur infinie ou NaN, et `TypeError`
    si une valeur n'est ni `int` ni `float` ou si c'est un booléen.
    """
    return _moyenne_exacte(_valider_niveaux(niveaux))


def _valider_niveaux(niveaux: Iterable[float]) -> list[float]:
    """Parcourt `niveaux` une seule fois et rend ses valeurs, contrôlées, en flottants."""
    try:
        iterateur = iter(niveaux)
    except TypeError:
        raise TypeError(
            "les niveaux doivent être fournis dans un itérable (liste, tuple, générateur...) : "
            f"reçu un objet de type {type(niveaux).__name__}"
        ) from None
    valeurs = []
    for indice, niveau in enumerate(iterateur):
        # Un booléen est un entier pour Python : il faut l'écarter avant le contrôle du type.
        if isinstance(niveau, bool):
            raise TypeError(
                f"niveau d'indice {indice} : un booléen ({niveau}) n'est pas un niveau sonore"
            )
        if not isinstance(niveau, (int, float)):
            raise TypeError(
                f"niveau d'indice {indice} : type {type(niveau).__name__} refusé, "
                "un nombre réel (int ou float) est attendu"
            )
        try:
            valeur = float(niveau)
        except OverflowError:
            raise ValueError(
                f"niveau d'indice {indice} : entier trop grand pour être converti en flottant"
            ) from None
        if math.isnan(valeur):
            raise ValueError(f"niveau d'indice {indice} : valeur indéfinie (NaN)")
        if math.isinf(valeur):
            raise ValueError(f"niveau d'indice {indice} : valeur infinie ({valeur})")
        valeurs.append(valeur)
    if not valeurs:
        raise ValueError("aucun niveau fourni : il en faut au moins un")
    return valeurs


def _niveau_des_energies(valeurs: list[float], diviseur: int) -> float:
    """Rend 10·log10((1/diviseur)·Σ 10^(Li/10)) en factorisant le niveau le plus élevé.

    Avec Lmax le plus grand des Li, Σ 10^(Li/10) = 10^(Lmax/10)·Σ 10^((Li - Lmax)/10), d'où

        L = Lmax + 10·log10((1/diviseur)·Σ 10^((Li - Lmax)/10)).

    Chaque terme de la somme est compris entre 0 et 1, et celui du maximum vaut 1 : aucun
    dépassement de capacité, quels que soient les niveaux (décision du journal : « Somme
    calculée en factorisant le niveau le plus élevé »). Le diviseur vaut 1 pour la somme
    énergétique et n pour la moyenne énergétique.
    """
    maximum = max(valeurs)
    # math.fsum additionne sans cumuler les erreurs d'arrondi. math.pow est préféré à l'opérateur
    # ** : le calcul est le même, mais quand le résultat est trop petit pour un flottant, le
    # module math rend cette valeur infime ou nulle sans jamais lever d'erreur, alors que
    # l'opérateur ** dépend sur ce point de la bibliothèque C de la plateforme.
    rapports = math.fsum(math.pow(10.0, (valeur - maximum) / 10.0) for valeur in valeurs)
    return maximum + 10.0 * math.log10(rapports / diviseur)


def _moyenne_exacte(valeurs: list[float]) -> float:
    """Rend le flottant le plus proche de la moyenne arithmétique exacte des valeurs.

    Un flottant fini est une fraction dont le dénominateur est une puissance de deux. Les
    numérateurs sont donc additionnés exactement, en entiers, dénominateur par dénominateur ; la
    division par n se fait en fractions, et il n'y a qu'un seul arrondi, à la toute fin. Aucun
    dépassement de capacité n'est possible : la moyenne est comprise entre le plus petit et le
    plus grand des niveaux.
    """
    numerateurs: dict[int, int] = {}
    for valeur in valeurs:
        numerateur, denominateur = valeur.as_integer_ratio()
        numerateurs[denominateur] = numerateurs.get(denominateur, 0) + numerateur
    somme = sum(
        Fraction(numerateur, denominateur) for denominateur, numerateur in numerateurs.items()
    )
    return float(somme / len(valeurs))
