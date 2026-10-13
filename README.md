# SUTOM / MOTUS — SAE 1.01 (Python)

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![SAE](https://img.shields.io/badge/SAE-S1.01-orange.svg)](#contexte-académique)
[![License](https://img.shields.io/badge/Status-Projet%20Universitaire-lightgrey.svg)](#auteurs-et-encadrement)

Implémentation complète en console du célèbre jeu de lettres **SUTOM** (inspiré de **Motus** et **Wordle**), développée en **Python** dans le cadre de la formation BUT Informatique.

---

## Sommaire

- [Présentation du projet](#-présentation-du-projet)
- [Règles du jeu](#-règles-du-jeu)
- [Fonctionnalités principales](#-fonctionnalités-principales)
- [Architecture du projet](#-architecture-du-projet)
- [Prérequis](#-prérequis)
- [Installation et Lancement](#-installation-et-lancement)
- [Système de scoring](#-système-de-scoring)
- [Contraintes académiques respectées](#-contraintes-académiques-respectées)
- [Auteurs et Encadrement](#-auteurs-et-encadrement)

---

## Présentation du projet

Ce projet a été réalisé dans le cadre de la **SAE 1.01 : Implémentation d'un besoin client** (Ressource R1.01) au département Informatique de l'IUT.

L'objectif est de proposer une application console complète, ergonomique et modulaire du jeu **SUTOM**, permettant de jouer seul (mots piochés aléatoirement dans un dictionnaire) ou à deux (un joueur choisit le mot secret), avec différents niveaux de difficulté et un système de sauvegarde des scores.

---

## Règles du jeu

Le but est de deviner un mot secret en un maximum de **6 tentatives** :

1. **Première lettre dévoilée** : Le mot commence obligatoirement par la lettre indiquée au début de la partie.
2. **Longueur fixe** : Chaque tentative doit comporter exactement le nombre de lettres requis (entre 2 et 15 lettres).
3. **Indices visuels par couleurs** (codes d'échappement ANSI) :
   - 🟥 **Rouge** : La lettre est **correcte et bien placée**.
   - 🟨 **Jaune** : La lettre est **présente dans le mot mais mal placée**.
   - ⬜ **Gris / Sans couleur** : La lettre est **absente du mot**.
4. **Gestion fine des doublons** : Le jeu évite le sur-comptage des lettres répétées grâce à un algorithme en deux passes (priorité aux lettres bien placées, puis marquage des lettres mal placées selon les occurrences restantes).

---

## Fonctionnalités principales

- **2 Modes de jeu** :
  - **Saisie manuelle** : Un joueur saisit le mot mystère (sans révélation) pour faire deviner un second joueur.
  - **Dictionnaire aléatoire** : Sélection automatique d'un mot secret parmi plus de **370 000 mots** de la langue française.
- **3 Niveaux de difficulté** :
  - **Facile** : Mots de 2 à 6 lettres.
  - **Moyen** : Mots de 7 à 10 lettres.
  - **Difficile** : Mots de 11 à 15 lettres.
- **Gestion des scores & Classement** :
  - Calcul dégressif des points selon le niveau et le nombre d'essais.
  - Sauvegarde persistante des scores dans un fichier (`data/scores.bin`).
  - Affichage d'un tableau d'honneur trié du meilleur au moins bon (tri à bulles).
  - Réinitialisation sécurisée avec mot de passe de confirmation (`REINITIALISER`).
- **Interface soignée dans le terminal** :
  - Titre en ASCII art.
  - Menu interactif et nettoyages d'écran.
  - Colorisation dynamique des lettres via codes ANSI.

---

## Architecture du projet

```text
Sutom/
├── Sujet/
│   └── sujet_S101_2025_2026.pdf   # Cahier des charges et consignes officielles de la SAE
├── data/
│   ├── dictionnaire.txt           # Dictionnaire de référence (378 000+ mots français)
│   ├── dictionnaires.txt          # Source dictionnaire
│   └── scores.bin                 # Fichier de persistance des pseudos et meilleurs scores
├── src/
│   ├── wordle.py                  # Point d'entrée principal : boucle de jeu, menu & interface ANSI
│   ├── definition_mot.py          # Module de gestion des mots (saisie, lecture du dico, sélection aléatoire)
│   └── gestion_score.py           # Module de persistance (sauvegarde, chargement, tri à bulles des scores)
├── requirements.txt               # Fichier des dépendances (bibliothèque standard Python uniquement)
└── README.md                      # Documentation du projet
```

---

## Prérequis

- **Python 3.10 ou supérieur** (requis pour la structure de contrôle structurel `match / case`).
- **Système d'exploitation** : Windows, Linux ou macOS.
- **Terminal avec support des couleurs ANSI**.

> **Note :** Aucune bibliothèque tierce (`pip`) n'est requise. Le projet utilise exclusivement les modules natifs de la bibliothèque standard Python (`os`, `random`).

---

## Installation et Lancement

### 1. Cloner ou télécharger le dépôt

```bash
git clone https://github.com/geoffreyrigal/Sutom.git
cd Sutom
```

### 2. Lancement du jeu

> ⚠️ **Important :** Le programme utilise des chemins relatifs vers le répertoire `data/` (`../data/...`). 
> Vous **devez impérativement vous placer dans le dossier `src`** avant d'exécuter le script.

```bash
cd src
python3 wordle.py
```

*(Sur Windows, utilisez `python wordle.py`)*

### 3. Navigation dans le jeu

Au lancement, un menu interactif vous propose :
- `1 - Jouer` : Démarre une nouvelle partie (choix du pseudo, du mode et du niveau).
- `2 - Afficher les scores` : Consulte le classement des meilleurs joueurs.
- `3 - Réinitialiser les scores` : Remet à zéro la base des scores (tapez `REINITIALISER` pour valider).
- `4 - Quitter` : Quitte proprement l'application.

---

## Système de scoring

Le score initial dépend du niveau de difficulté sélectionné :

| Niveau | Longueur du mot | Score maximal (1er essai) |
| :--- | :--- | :--- |
| **Facile** | 2 à 6 lettres | **10 000 points** |
| **Moyen** | 7 à 10 lettres | **30 000 points** |
| **Difficile** | 11 à 15 lettres | **50 000 points** |

À chaque tentative infructueuse, le score potentiel diminue de **20%** :
$$\text{Score final} = \text{Score initial} \times (0.8)^{\text{tentatives} - 1}$$

En cas de défaite (6 tentatives épuisées sans trouver le mot), aucun point n'est attribué.

---

## Contraintes académiques respectées

Conformément aux directives de la ressource **R1.01** et du sujet de la SAE :

- **Conception modulaire** : Séparation stricte des responsabilités en trois modules indépendants (`wordle.py`, `definition_mot.py`, `gestion_score.py`).
- **Typage statique systématique** : Toutes les variables locales, paramètres de fonctions et valeurs de retour sont explicitement typés (`int`, `str`, `list`, `bool`, etc.).
- **Documentation et spécifications** : Chaque fonction possède une docstring détaillée avec ses pré-conditions et post-conditions (entrées/sorties).
- **Bibliothèques restreintes** : Utilisation exclusive du module `os` et des mécanismes natifs (codes ANSI, algorithme de tri à bulles fait maison sans `list.sort()`).
- **Robustesse des saisies** : Validation systématique de toutes les entrées utilisateurs (menus, longueur de mot, première lettre, confirmations).

---

## Auteurs

- **Projet réalisé par :** Rigal Geoffrey et Dartevelle Samuel.
