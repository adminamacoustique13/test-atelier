"""Tests des calculs sur les niveaux sonores.

La classe `TestCriteres` reprend un par un les critères 1 à 17 de la tâche B du cahier des
charges (chantier/CAHIER.md), avec les valeurs de référence et les tolérances qui y sont écrites.
Les classes suivantes complètent la preuve : comparaison à un calcul de référence indépendant en
haute précision, propriétés générales, valeurs extrêmes, arrondis, et choix que la consigne ne
tranchait pas.

À lancer depuis la racine du dépôt : python3 -m unittest discover -s tests -v
"""

import math
import random
import sys
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction

import decibels
from decibels import moyenne_arithmetique, moyenne_energetique, somme_niveaux

FONCTIONS = (somme_niveaux, moyenne_energetique, moyenne_arithmetique)

# Calcul de référence : nombre de chiffres décimaux et tolérance de comparaison.
PRECISION = 60
TOLERANCE = Decimal("1e-9")
DIX = Decimal(10)


def _reference_somme(niveaux):
    """Somme énergétique par la formule directe, sans factorisation, en décimal."""
    with localcontext() as contexte:
        contexte.prec = PRECISION
        energies = [DIX ** (Decimal(niveau) / DIX) for niveau in niveaux]
        return DIX * sum(energies).log10()


def _reference_moyenne_energetique(niveaux):
    """Moyenne énergétique par la formule directe, sans factorisation, en décimal."""
    with localcontext() as contexte:
        contexte.prec = PRECISION
        energies = [DIX ** (Decimal(niveau) / DIX) for niveau in niveaux]
        return DIX * (sum(energies) / len(energies)).log10()


def _reference_moyenne_arithmetique(niveaux):
    """Moyenne arithmétique en décimal."""
    with localcontext() as contexte:
        contexte.prec = PRECISION
        return sum(Decimal(niveau) for niveau in niveaux) / len(niveaux)


def _ecart(valeur, reference):
    """Écart absolu entre un flottant et une valeur de référence décimale."""
    with localcontext() as contexte:
        contexte.prec = PRECISION
        return abs(Decimal(valeur) - reference)


def _moyenne_en_fractions(niveaux):
    """Flottant le plus proche de la moyenne arithmétique exacte, calculée en fractions."""
    return float(sum(Fraction(niveau) for niveau in niveaux) / len(niveaux))


def _decaler(valeur, crans):
    """Rend le flottant situé `crans` crans au-dessus de `valeur`."""
    for _ in range(crans):
        valeur = math.nextafter(valeur, math.inf)
    return valeur


def _tirer(hasard, famille, taille):
    """Tire une liste de `taille` niveaux dans la famille demandée."""
    if famille == "courants":
        return [hasard.uniform(-20.0, 140.0) for _ in range(taille)]
    if famille == "entiers":
        return [hasard.randint(0, 130) for _ in range(taille)]
    if famille == "etendus":
        return [hasard.uniform(-4000.0, 4000.0) for _ in range(taille)]
    if famille == "serres":
        centre = hasard.uniform(-20.0, 140.0)
        return [centre + hasard.uniform(-1e-6, 1e-6) for _ in range(taille)]
    if famille == "voisins":
        base = hasard.choice((-1.0, 1.0)) * 10.0 ** hasard.uniform(0.0, 10.0)
        return [_decaler(base, hasard.randint(0, 3)) for _ in range(taille)]
    if famille == "immenses":
        return [hasard.uniform(-1e12, 1e12) for _ in range(taille)]
    raise ValueError(f"famille inconnue : {famille}")


def _listes_au_hasard(graine, nombre, familles):
    """Rend `nombre` listes de niveaux, toujours les mêmes pour une graine donnée."""
    hasard = random.Random(graine)
    return [
        _tirer(hasard, familles[rang % len(familles)], hasard.randint(1, 25))
        for rang in range(nombre)
    ]


def _generateur_temoin(niveaux, tirages):
    """Générateur qui note dans `tirages` chaque valeur qu'il fournit."""
    for niveau in niveaux:
        tirages.append(niveau)
        yield niveau


class _IterableCompte:
    """Itérable, autre qu'une liste, qui compte le nombre de fois où on le parcourt."""

    def __init__(self, niveaux):
        self._niveaux = tuple(niveaux)
        self.parcours = 0

    def __iter__(self):
        self.parcours += 1
        return iter(self._niveaux)


class _Flottant(float):
    """Sous-classe de `float`, comme en fournissent certaines bibliothèques de calcul."""


class _Entier(int):
    """Sous-classe de `int`."""


class TestCriteres(unittest.TestCase):
    """Les critères 1 à 17 du cahier des charges, dans l'ordre."""

    def test_critere_01_somme_de_60_et_60(self):
        """Critère 1 : somme_niveaux([60, 60]) vaut 63,0103 à 1e-4 près."""
        self.assertAlmostEqual(somme_niveaux([60, 60]), 63.0103, delta=1e-4)

    def test_critere_02_somme_de_60_et_70(self):
        """Critère 2 : somme_niveaux([60, 70]) vaut 70,41393 à 1e-5 près."""
        self.assertAlmostEqual(somme_niveaux([60, 70]), 70.41393, delta=1e-5)

    def test_critere_03_somme_de_dix_niveaux_de_50(self):
        """Critère 3 : somme_niveaux de dix niveaux de 50 dB vaut 60,0 à 1e-9 près."""
        self.assertAlmostEqual(somme_niveaux([50] * 10), 60.0, delta=1e-9)
        self.assertAlmostEqual(somme_niveaux([50.0] * 10), 60.0, delta=1e-9)

    def test_critere_04_somme_d_un_seul_niveau(self):
        """Critère 4 : somme_niveaux([x]) vaut x à 1e-9 près, pour un seul niveau."""
        for x in (0, 1, 60, 94, 37.25, 60.1, 120.5, -10, -0.1, 1e-12, 4000, -4000, 1e15, -1e15):
            with self.subTest(x=x):
                self.assertAlmostEqual(somme_niveaux([x]), x, delta=1e-9)

    def test_critere_05_moyenne_energetique_de_60_et_70(self):
        """Critère 5 : moyenne_energetique([60, 70]) vaut 67,40363 à 1e-5 près."""
        self.assertAlmostEqual(moyenne_energetique([60, 70]), 67.40363, delta=1e-5)

    def test_critere_06_moyenne_energetique_de_niveaux_egaux(self):
        """Critère 6 : moyenne_energetique de niveaux tous égaux à x vaut x à 1e-9 près."""
        for x in (0, 60, 94, 37.25, 60.1, -10, -0.1, 4000, -4000, 1e15, -1e15):
            for nombre in (1, 2, 3, 7, 10, 1000):
                with self.subTest(x=x, nombre=nombre):
                    self.assertAlmostEqual(moyenne_energetique([x] * nombre), x, delta=1e-9)

    def test_critere_07_moyenne_arithmetique_de_60_et_70(self):
        """Critère 7 : moyenne_arithmetique([60, 70]) vaut 65,0."""
        self.assertEqual(moyenne_arithmetique([60, 70]), 65.0)
        self.assertEqual(moyenne_arithmetique([60.0, 70.0]), 65.0)

    def test_critere_08_moyenne_energetique_au_moins_egale_a_l_arithmetique(self):
        """Critère 8 : pour toute liste, moyenne énergétique >= moyenne arithmétique - 1e-9."""
        familles = ("courants", "entiers", "etendus", "serres", "voisins", "immenses")
        listes = _listes_au_hasard(graine=8, nombre=600, familles=familles)
        listes += [[60, 70], [0, 100], [-4000, 4000], [50] * 10, [61.3], [60, 60, 60, 90]]
        # Flottants voisins de très grande valeur : l'écart entre eux dépasse la tolérance.
        listes += [
            [100000000.00000001, 100000000.00000003],
            [-99999999.99999999, -99999999.99999997],
        ]
        for niveaux in listes:
            with self.subTest(niveaux=niveaux):
                self.assertGreaterEqual(
                    moyenne_energetique(niveaux), moyenne_arithmetique(niveaux) - 1e-9
                )

    def test_critere_09_somme_de_niveaux_de_4000(self):
        """Critère 9 : somme_niveaux([4000, 4000]) vaut 4003,0103 à 1e-4 près, sans dépassement."""
        self.assertAlmostEqual(somme_niveaux([4000, 4000]), 4003.0103, delta=1e-4)

    def test_critere_10_somme_de_niveaux_de_moins_4000(self):
        """Critère 10 : somme_niveaux([-4000, -4000]) vaut -3996,9897 à 1e-4 près."""
        self.assertAlmostEqual(somme_niveaux([-4000, -4000]), -3996.9897, delta=1e-4)

    def test_critere_11_generateur_parcouru_une_seule_fois(self):
        """Critère 11 : les trois fonctions acceptent un générateur, parcouru une seule fois."""
        niveaux = [60, 70, 55.5, 62, -3]
        for fonction in FONCTIONS:
            with self.subTest(fonction=fonction.__name__, source="fonction génératrice"):
                tirages = []
                generateur = _generateur_temoin(niveaux, tirages)
                self.assertEqual(fonction(generateur), fonction(niveaux))
                # Chaque valeur a été demandée une fois, dans l'ordre, et il n'en reste aucune.
                self.assertEqual(tirages, niveaux)
                self.assertEqual(list(generateur), [])
            with self.subTest(fonction=fonction.__name__, source="expression génératrice"):
                generateur = (niveau for niveau in niveaux)
                self.assertEqual(fonction(generateur), fonction(niveaux))
                self.assertEqual(list(generateur), [])
            with self.subTest(fonction=fonction.__name__, source="itérable compté"):
                iterable = _IterableCompte(niveaux)
                self.assertEqual(fonction(iterable), fonction(niveaux))
                self.assertEqual(iterable.parcours, 1)

    def test_critere_12_entree_vide(self):
        """Critère 12 : une entrée vide lève ValueError."""
        vides = (
            ("liste", list),
            ("tuple", tuple),
            ("itérateur", lambda: iter([])),
            ("générateur", lambda: (niveau for niveau in [])),
            ("range", lambda: range(0)),
        )
        for fonction in FONCTIONS:
            for nom, fabrique in vides:
                with (
                    self.subTest(fonction=fonction.__name__, entree=nom),
                    self.assertRaises(ValueError),
                ):
                    fonction(fabrique())

    def test_critere_13_valeur_ni_int_ni_float(self):
        """Critère 13 : une valeur qui n'est ni int ni float lève TypeError."""
        intrus = ("60", None, 60 + 0j, Decimal(60), Fraction(60), [60], (60,), b"<", object())
        for fonction in FONCTIONS:
            for valeur in intrus:
                for niveaux in ([valeur], [valeur, 60], [60, valeur], [60, valeur, 70.5]):
                    with (
                        self.subTest(fonction=fonction.__name__, niveaux=niveaux),
                        self.assertRaises(TypeError),
                    ):
                        fonction(niveaux)

    def test_critere_14_booleen(self):
        """Critère 14 : un booléen lève TypeError."""
        for fonction in FONCTIONS:
            for valeur in (True, False):
                for niveaux in ([valeur], [valeur, 60], [60, valeur], [60.5, valeur, 70]):
                    with (
                        self.subTest(fonction=fonction.__name__, niveaux=niveaux),
                        self.assertRaises(TypeError),
                    ):
                        fonction(niveaux)

    def test_critere_15_valeur_infinie(self):
        """Critère 15 : une valeur infinie lève ValueError."""
        for fonction in FONCTIONS:
            for valeur in (math.inf, -math.inf, float("inf"), float("-inf"), 1e308 * 10):
                for niveaux in ([valeur], [valeur, 60], [60, valeur], [60, valeur, 70.5]):
                    with (
                        self.subTest(fonction=fonction.__name__, niveaux=niveaux),
                        self.assertRaises(ValueError),
                    ):
                        fonction(niveaux)

    def test_critere_16_valeur_nan(self):
        """Critère 16 : une valeur NaN lève ValueError."""
        for fonction in FONCTIONS:
            for valeur in (math.nan, -math.nan, float("nan"), math.inf - math.inf):
                for niveaux in ([valeur], [valeur, 60], [60, valeur], [60, valeur, 70.5]):
                    with (
                        self.subTest(fonction=fonction.__name__, niveaux=niveaux),
                        self.assertRaises(ValueError),
                    ):
                        fonction(niveaux)

    def test_critere_17_niveaux_negatifs(self):
        """Critère 17 : niveaux négatifs acceptés, somme_niveaux([-10, -10]) = -6,9897 à 1e-4."""
        self.assertAlmostEqual(somme_niveaux([-10, -10]), -6.9897, delta=1e-4)
        # Les deux moyennes acceptent elles aussi des niveaux négatifs.
        self.assertAlmostEqual(moyenne_energetique([-10, -10]), -10.0, delta=1e-9)
        self.assertAlmostEqual(moyenne_arithmetique([-10, -20]), -15.0, delta=1e-9)


class TestCalculDeReference(unittest.TestCase):
    """Comparaison à un calcul indépendant : formule directe, décimal à 60 chiffres."""

    FAMILLES = ("courants", "entiers", "etendus", "serres")

    def test_la_reference_retrouve_les_valeurs_de_la_consigne(self):
        """Le calcul de référence donne les valeurs écrites dans les critères."""
        cas = (
            (_reference_somme([60, 60]), "63.0103", "1e-4"),
            (_reference_somme([60, 70]), "70.41393", "1e-5"),
            (_reference_somme([50] * 10), "60", "1e-9"),
            (_reference_moyenne_energetique([60, 70]), "67.40363", "1e-5"),
            (_reference_moyenne_arithmetique([60, 70]), "65", "0"),
            (_reference_somme([4000, 4000]), "4003.0103", "1e-4"),
            (_reference_somme([-4000, -4000]), "-3996.9897", "1e-4"),
            (_reference_somme([-10, -10]), "-6.9897", "1e-4"),
        )
        for reference, attendu, tolerance in cas:
            with self.subTest(attendu=attendu):
                self.assertLessEqual(abs(reference - Decimal(attendu)), Decimal(tolerance))

    def test_somme_niveaux(self):
        """somme_niveaux suit la formule directe à 1e-9 près sur 240 listes tirées au hasard."""
        for niveaux in _listes_au_hasard(graine=1, nombre=240, familles=self.FAMILLES):
            with self.subTest(niveaux=niveaux):
                ecart = _ecart(somme_niveaux(niveaux), _reference_somme(niveaux))
                self.assertLessEqual(ecart, TOLERANCE)

    def test_moyenne_energetique(self):
        """moyenne_energetique suit la formule directe à 1e-9 près sur 240 listes."""
        for niveaux in _listes_au_hasard(graine=2, nombre=240, familles=self.FAMILLES):
            with self.subTest(niveaux=niveaux):
                reference = _reference_moyenne_energetique(niveaux)
                self.assertLessEqual(_ecart(moyenne_energetique(niveaux), reference), TOLERANCE)

    def test_moyenne_arithmetique(self):
        """moyenne_arithmetique suit la formule directe à 1e-9 près sur 240 listes."""
        for niveaux in _listes_au_hasard(graine=3, nombre=240, familles=self.FAMILLES):
            with self.subTest(niveaux=niveaux):
                reference = _reference_moyenne_arithmetique(niveaux)
                self.assertLessEqual(_ecart(moyenne_arithmetique(niveaux), reference), TOLERANCE)

    def test_cas_d_ecole(self):
        """Quelques résultats connus de l'addition des niveaux."""
        # Cent sources égales : + 20 dB. Mille : + 30 dB.
        self.assertAlmostEqual(somme_niveaux([40] * 100), 60.0, delta=1e-9)
        self.assertAlmostEqual(somme_niveaux([40] * 1000), 70.0, delta=1e-9)
        # Trois sources égales : + 10·log10(3) = 4,771213 dB.
        self.assertAlmostEqual(somme_niveaux([80, 80, 80]), 84.771213, delta=1e-6)
        # Une source 10 dB plus faible ajoute 0,413927 dB ; 20 dB plus faible, 0,043214 dB.
        self.assertAlmostEqual(somme_niveaux([90, 80]), 90.413927, delta=1e-6)
        self.assertAlmostEqual(somme_niveaux([90, 70]), 90.043214, delta=1e-6)
        # Moyenne énergétique de 0 dB et 100 dB : 100 - 10·log10(2) à très peu près.
        self.assertAlmostEqual(moyenne_energetique([0, 100]), 96.989700, delta=1e-6)
        self.assertEqual(moyenne_arithmetique([0, 100]), 50.0)
        self.assertEqual(moyenne_arithmetique([60, 61, 65]), 62.0)


class TestProprietes(unittest.TestCase):
    """Propriétés qui découlent des définitions, vérifiées sur des listes tirées au hasard."""

    FAMILLES = ("courants", "entiers", "etendus", "serres")

    def test_ordre_des_niveaux_sans_effet(self):
        """Le résultat ne dépend pas de l'ordre des niveaux, au bit près."""
        hasard = random.Random(4)
        listes = _listes_au_hasard(graine=4, nombre=120, familles=self.FAMILLES)
        # Un niveau dominant et dix mille niveaux infimes : une addition faite terme après terme
        # donnerait un résultat différent selon que le niveau dominant vient en tête ou en queue.
        listes.append([100.0] + [-60.0] * 10_000)
        for niveaux in listes:
            melange = list(niveaux)
            hasard.shuffle(melange)
            for fonction in FONCTIONS:
                with self.subTest(fonction=fonction.__name__, taille=len(niveaux)):
                    attendu = fonction(niveaux)
                    self.assertEqual(fonction(melange), attendu)
                    self.assertEqual(fonction(niveaux[::-1]), attendu)

    def test_moyenne_energetique_et_somme(self):
        """Moyenne énergétique = somme énergétique - 10·log10(n)."""
        for niveaux in _listes_au_hasard(graine=5, nombre=120, familles=self.FAMILLES):
            with self.subTest(niveaux=niveaux):
                attendu = somme_niveaux(niveaux) - 10 * math.log10(len(niveaux))
                self.assertAlmostEqual(moyenne_energetique(niveaux), attendu, delta=1e-9)

    def test_decalage_de_tous_les_niveaux(self):
        """Ajouter une même valeur à tous les niveaux l'ajoute au résultat."""
        for niveaux in _listes_au_hasard(graine=6, nombre=120, familles=("courants", "entiers")):
            for decalage in (-37.5, 3, 250):
                decales = [niveau + decalage for niveau in niveaux]
                for fonction in FONCTIONS:
                    with self.subTest(fonction=fonction.__name__, niveaux=niveaux):
                        attendu = fonction(niveaux) + decalage
                        self.assertAlmostEqual(fonction(decales), attendu, delta=1e-9)

    def test_bornes(self):
        """max <= somme <= max + 10·log10(n), et min <= arithmétique <= énergétique <= max."""
        familles = ("courants", "entiers", "etendus", "serres", "voisins", "immenses")
        for niveaux in _listes_au_hasard(graine=7, nombre=300, familles=familles):
            with self.subTest(niveaux=niveaux):
                plus_petit, plus_grand = float(min(niveaux)), float(max(niveaux))
                somme = somme_niveaux(niveaux)
                self.assertGreaterEqual(somme, plus_grand)
                self.assertLessEqual(somme, plus_grand + 10 * math.log10(len(niveaux)) + 1e-9)
                arithmetique = moyenne_arithmetique(niveaux)
                energetique = moyenne_energetique(niveaux)
                self.assertLessEqual(plus_petit, arithmetique)
                self.assertLessEqual(arithmetique, energetique)
                self.assertLessEqual(energetique, plus_grand)

    def test_doublement_de_la_liste(self):
        """Doubler toutes les sources ajoute 10·log10(2) à la somme et ne change pas les moyennes."""
        for niveaux in _listes_au_hasard(graine=9, nombre=120, familles=self.FAMILLES):
            with self.subTest(niveaux=niveaux):
                double = niveaux + niveaux
                attendu = somme_niveaux(niveaux) + 10 * math.log10(2)
                self.assertAlmostEqual(somme_niveaux(double), attendu, delta=1e-9)
                self.assertAlmostEqual(
                    moyenne_energetique(double), moyenne_energetique(niveaux), delta=1e-9
                )
                self.assertEqual(moyenne_arithmetique(double), moyenne_arithmetique(niveaux))


class TestValeursExtremes(unittest.TestCase):
    """Aucun dépassement de capacité, quels que soient les niveaux finis fournis."""

    PLUS_GRAND = sys.float_info.max
    PLUS_PETIT = 5e-324

    def test_niveaux_tres_ecartes(self):
        """Des niveaux écartés de 8000 dB : le plus faible ne compte plus, sans erreur."""
        self.assertEqual(somme_niveaux([4000, -4000]), 4000.0)
        self.assertEqual(somme_niveaux([-4000, 4000]), 4000.0)
        attendu = 4000 - 10 * math.log10(2)
        self.assertAlmostEqual(moyenne_energetique([4000, -4000]), attendu, delta=1e-9)
        self.assertEqual(moyenne_arithmetique([4000, -4000]), 0.0)

    def test_moyennes_de_niveaux_de_4000(self):
        """Les deux moyennes supportent aussi les niveaux des critères 9 et 10."""
        for fonction in (moyenne_energetique, moyenne_arithmetique):
            with self.subTest(fonction=fonction.__name__):
                self.assertEqual(fonction([4000, 4000]), 4000.0)
                self.assertEqual(fonction([-4000, -4000]), -4000.0)

    def test_ecarts_ou_la_puissance_de_dix_devient_minuscule(self):
        """Écarts de 3070 à 3250 dB : 10^(-écart/10) s'approche puis atteint zéro, sans erreur."""
        for ecart in (3070, 3080, 3100, 3200, 3230, 3233, 3234, 3240, 3250):
            with self.subTest(ecart=ecart):
                self.assertEqual(somme_niveaux([0, -ecart]), 0.0)
                self.assertEqual(somme_niveaux([ecart, 0]), float(ecart))
                attendu = -10 * math.log10(2)
                self.assertAlmostEqual(moyenne_energetique([0, -ecart]), attendu, delta=1e-9)

    def test_plus_grands_flottants(self):
        """Les plus grands flottants possibles ne provoquent aucun dépassement."""
        grand = self.PLUS_GRAND
        for fonction in FONCTIONS:
            with self.subTest(fonction=fonction.__name__):
                self.assertEqual(fonction([grand, grand]), grand)
                self.assertEqual(fonction([-grand, -grand, -grand]), -grand)
        self.assertEqual(somme_niveaux([grand, -grand]), grand)
        self.assertEqual(moyenne_energetique([grand, -grand]), grand)
        self.assertEqual(moyenne_arithmetique([grand, -grand]), 0.0)
        self.assertEqual(moyenne_arithmetique([grand, grand, -grand]), grand / 3)

    def test_plus_petits_flottants(self):
        """Les plus petits flottants non nuls se comportent comme zéro décibel."""
        petit = self.PLUS_PETIT
        self.assertAlmostEqual(somme_niveaux([petit, -petit]), 10 * math.log10(2), delta=1e-9)
        self.assertAlmostEqual(moyenne_energetique([petit, -petit]), 0.0, delta=1e-9)
        self.assertEqual(moyenne_arithmetique([petit, -petit]), 0.0)
        self.assertEqual(moyenne_arithmetique([petit, petit]), petit)
        self.assertEqual(moyenne_arithmetique([petit, 3 * petit]), 2 * petit)

    def test_longue_liste(self):
        """Cent mille niveaux égaux : + 50 dB pour la somme, moyennes inchangées."""
        niveaux = [35.5] * 100_000
        self.assertAlmostEqual(somme_niveaux(niveaux), 85.5, delta=1e-9)
        self.assertEqual(moyenne_energetique(niveaux), 35.5)
        self.assertEqual(moyenne_arithmetique(niveaux), 35.5)


class TestArrondis(unittest.TestCase):
    """Ce que les fonctions garantissent au dernier chiffre près."""

    def test_un_seul_niveau_rendu_tel_quel(self):
        """Avec un seul niveau, les trois fonctions rendent ce niveau exactement."""
        for x in (60, 60.1, -0.1, 1e-300, 123456.789, 4000.0000000000005, 1e15, -1e300):
            for fonction in FONCTIONS:
                with self.subTest(fonction=fonction.__name__, x=x):
                    self.assertEqual(fonction([x]), x)

    def test_niveaux_egaux_rendus_tels_quels(self):
        """Les moyennes de niveaux tous égaux à x valent exactement x, même pour x immense."""
        # 1.5000000000000004 : la somme de trois exemplaires, divisée par trois, tombe à côté.
        for x in (60.1, 1.5000000000000004, -37.25, 94.03, 123456789.12345679, 1e300):
            for nombre in (2, 3, 5, 7, 10, 49):
                with self.subTest(x=x, nombre=nombre):
                    self.assertEqual(moyenne_arithmetique([x] * nombre), x)
                    self.assertEqual(moyenne_energetique([x] * nombre), x)

    def test_niveaux_infimes_un_par_un_mais_pas_ensemble(self):
        """Dix mille niveaux 160 dB sous le plus fort : chacun est infime, leur total compte."""
        # Chacun apporte 1e-16 fois l'énergie du niveau dominant, moins que le dernier chiffre
        # d'un flottant ; ensemble ils apportent 1e-12, soit 10·log10(1 + 1e-12) décibels.
        niveaux = [100.0] + [-60.0] * 10_000
        attendu = 100.0 + 10 * math.log10(1 + 1e-12)
        self.assertAlmostEqual(somme_niveaux(niveaux), attendu, delta=1e-12)
        self.assertGreater(somme_niveaux(niveaux), 100.0)

    def test_moyenne_arithmetique_arrondie_au_plus_proche(self):
        """moyenne_arithmetique rend le flottant le plus proche de la moyenne exacte."""
        familles = ("courants", "entiers", "etendus", "serres", "voisins", "immenses")
        listes = _listes_au_hasard(graine=10, nombre=600, familles=familles)
        listes += [[0.1, 0.2, 0.3], [1e16, 1.0, -1e16], [1e308, 1e308, -1e308], [5e-324] * 3]
        for niveaux in listes:
            with self.subTest(niveaux=niveaux):
                self.assertEqual(moyenne_arithmetique(niveaux), _moyenne_en_fractions(niveaux))

    def test_moyenne_energetique_jamais_sous_l_arithmetique(self):
        """Sans aucune tolérance : moyenne énergétique >= moyenne arithmétique."""
        # Deux flottants voisins : leur moyenne arithmétique tombe pile entre les deux et
        # s'arrondit au second, la moyenne énergétique est à peine plus haute. Le calcul en
        # logarithme, lui, peut s'arrondir au premier.
        for depart in (4.0, 16.0, 60.0, 128.0, 1000.0, 4000.0, 1e6, 2.0**25, 1e8):
            bas = _decaler(depart, 1)
            haut = _decaler(depart, 2)
            for niveaux in ([bas, haut], [haut, bas]):
                with self.subTest(niveaux=niveaux):
                    self.assertEqual(moyenne_arithmetique(niveaux), haut)
                    self.assertEqual(moyenne_energetique(niveaux), haut)
        listes = _listes_au_hasard(graine=11, nombre=900, familles=("voisins", "serres"))
        for niveaux in listes:
            with self.subTest(niveaux=niveaux):
                self.assertGreaterEqual(moyenne_energetique(niveaux), moyenne_arithmetique(niveaux))


class TestChoixHorsConsigne(unittest.TestCase):
    """Comportements que la consigne ne tranchait pas (voir chantier/relais/B.md)."""

    def test_resultat_de_type_float(self):
        """Le résultat est un `float` ordinaire, quels que soient les nombres fournis."""
        entrees = (
            [60, 70],
            [60.0, 70.0],
            [60, 70.5],
            [60],
            [_Flottant(60.5), _Flottant(70.25)],
            [_Entier(60), _Entier(70)],
        )
        for fonction in FONCTIONS:
            for niveaux in entrees:
                with self.subTest(fonction=fonction.__name__, niveaux=niveaux):
                    self.assertIs(type(fonction(niveaux)), float)

    def test_entiers_et_flottants_equivalents(self):
        """Des entiers donnent le même résultat que les flottants de même valeur."""
        for fonction in FONCTIONS:
            with self.subTest(fonction=fonction.__name__):
                attendu = fonction([60.0, 70.0, 55.0])
                self.assertEqual(fonction([60, 70, 55]), attendu)
                self.assertEqual(fonction([60, 70.0, 55]), attendu)
                self.assertEqual(fonction((60, 70, 55)), attendu)
                self.assertEqual(fonction([_Entier(60), _Flottant(70.0), 55]), attendu)

    def test_sous_classes_de_float_et_int_acceptees(self):
        """Une sous-classe de `float` ou de `int`, hors booléen, est acceptée."""
        self.assertAlmostEqual(somme_niveaux([_Flottant(60.0), _Entier(60)]), 63.0103, delta=1e-4)

    def test_entier_trop_grand_pour_un_flottant(self):
        """Un entier qu'aucun flottant ne peut représenter lève ValueError."""
        for fonction in FONCTIONS:
            for niveaux in ([10**400], [60, 10**400], [-(10**400), 60]):
                with self.subTest(fonction=fonction.__name__), self.assertRaises(ValueError):
                    fonction(niveaux)

    def test_argument_non_iterable(self):
        """Un argument qui n'est pas un itérable lève TypeError, avec un message en français."""
        for fonction in FONCTIONS:
            for argument in (60, 60.5, None, True):
                with (
                    self.subTest(fonction=fonction.__name__, argument=argument),
                    self.assertRaisesRegex(TypeError, "dans un itérable"),
                ):
                    fonction(argument)

    def test_chaine_de_caracteres(self):
        """Une chaîne, même faite de chiffres, lève TypeError."""
        for fonction in FONCTIONS:
            for argument in ("60", "60 70", ["60", "70"]):
                with (
                    self.subTest(fonction=fonction.__name__, argument=argument),
                    self.assertRaises(TypeError),
                ):
                    fonction(argument)

    def test_message_d_erreur_en_francais_avec_l_indice(self):
        """Le message d'erreur dit, en français, quel niveau est refusé et pourquoi."""
        cas = (
            (TypeError, [60, 70, "80"], "indice 2", "str"),
            (TypeError, [60, True], "indice 1", "booléen"),
            (ValueError, [math.nan, 60], "indice 0", "NaN"),
            (ValueError, [60, 61, 62, -math.inf], "indice 3", "infinie"),
            (ValueError, [], "aucun niveau", "au moins un"),
        )
        for fonction in FONCTIONS:
            for erreur, niveaux, *fragments in cas:
                with self.subTest(fonction=fonction.__name__, niveaux=niveaux):
                    with self.assertRaises(erreur) as contexte:
                        fonction(niveaux)
                    for fragment in fragments:
                        self.assertIn(fragment, str(contexte.exception))

    def test_entree_non_modifiee(self):
        """La liste fournie n'est pas modifiée."""
        niveaux = [70, 60.5, 55, 62]
        copie = list(niveaux)
        for fonction in FONCTIONS:
            fonction(niveaux)
            self.assertEqual(niveaux, copie)
            self.assertEqual([type(niveau) for niveau in niveaux], [int, float, int, int])


class TestContratDImport(unittest.TestCase):
    """Le contrat : `from decibels import somme_niveaux, moyenne_energetique, ...`."""

    def test_trois_fonctions_exportees(self):
        """Le paquet exporte les trois fonctions, et elles seules."""
        attendu = ["moyenne_arithmetique", "moyenne_energetique", "somme_niveaux"]
        self.assertEqual(sorted(decibels.__all__), attendu)
        for nom in attendu:
            with self.subTest(nom=nom):
                self.assertTrue(callable(getattr(decibels, nom)))
                self.assertIs(getattr(decibels, nom), getattr(decibels.niveaux, nom))
