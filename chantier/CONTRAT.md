# Contrat de chantier — 2026-11-11

État : validé par la personne responsable le 2026-11-11.

## Objectif
Livrer une petite bibliothèque Python, sans dépendance, qui additionne et moyenne des niveaux sonores exprimés en décibels, accompagnée de tests qui prouvent la justesse des calculs.

## Ce que la bibliothèque fera
- Somme de niveaux : addition des énergies, soit L = 10·log10(Σ 10^(Li/10)). Deux sources de 60 dB donnent 63,01 dB.
- Moyenne énergétique : même calcul, divisé par le nombre de niveaux. C'est la moyenne d'usage en acoustique.
- Moyenne arithmétique : simple moyenne des valeurs en dB, fournie à part et nommée sans ambiguïté, parce que certaines méthodes de mesure la demandent.
- Entrées refusées avec un message clair : liste vide, valeur qui n'est pas un nombre, valeur infinie ou indéfinie.

## Hors périmètre
- Pondérations fréquentielles (A, C), bandes d'octave, niveaux équivalents pondérés par la durée.
- Publication du paquet, interface en ligne de commande, documentation au-delà d'un court mode d'emploi.
- Les fichiers de la méthode : `CLAUDE.md`, `.claude/`.

## Découpage prévu
- Tâche A : squelette du paquet (configuration, dossiers, mode d'emploi). Mécanique.
- Tâche B : les trois fonctions de calcul et leurs tests. Formule scientifique, donc ouvrier et vérificateur au plus haut dès le départ.

## Enveloppe
- Agents lancés au maximum : 6
- Tentatives par tâche au maximum : 3
- Montées en gamme au maximum : 2

## Plafond d'escalade
Fable en effort max (`ouvrier-physique`, vérifié par `verificateur-fable-max`).

## Zones rouges
- Changer un choix d'architecture inscrit au journal.
- Supprimer des fichiers ou réécrire l'historique git.
- Déployer ou pousser en production ; pousser sur `main`.
- Toucher aux secrets.
- Installer une dépendance ou un plugin nouveau.
- Modifier les tests de référence ou les garde-fous eux-mêmes.
