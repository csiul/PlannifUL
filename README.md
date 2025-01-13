# Vérification des conflits d'horaire de cours

Ce script permet de vérifier si une plage horaire donnée entre en conflit avec des horaires de cours existants pour un ou plusieurs départements de l'Université Laval.

## Prérequis

- Python 3.7 ou version ultérieure
- Accès à Internet pour récupérer les données de CapsuleWeb

## Installation

1. Clonez le dépôt ou téléchargez le script.
2. Assurez-vous d'avoir Python et `pip` installés sur votre machine.
3. Installez les dépendances Python nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

## Utilisation
### Lancer le script

Utilisez la commande suivante pour exécuter le script :
```bash
python main.py -y <année> -s <semestre> -d <départements> -t <plage_horaire> -w <jour>
```

### Arguments requis
- -y, --year : Année du trimestre (exemple : 2025).
- -s, --semester : Semestre (1 pour Hiver, 5 pour Été, 9 pour Automne).
- -d, --departments : Liste des départements à analyser (par défaut : IFT et GLO).
- -t, --time : Plage horaire choisie au format HH:MM - HH:MM (exemple : 18:00 - 21:00).
- -w, --weekday : Jour de la semaine (L pour Lundi, M pour Mardi, R pour Mercredi, J pour Jeudi, V pour Vendredi).

## Exemple d'utilisation
### Vérifier les conflits pour un cours donné
Pour vérifier si une plage horaire donnée est en conflit avec des cours de l'IFT et du GLO durant le trimestre d'hiver 2025 :
```bash
python main.py -y 2025 -s 1 -d IFT GLO GIF -t "18:00 - 21:00" -w L
```

## Résultats
Le script affiche les cours en conflit avec la plage horaire spécifiée. Par exemple :
```
Conflit avec Algorithmique et programmation - 15900 - IFT 1004 - Z3 à 18:30 - 19:50
Conflit avec Programmation avancée en C++ - 15901 - IFT 1006 - Z3 à 16:00 - 18:50
Conflit avec Qualité logicielle en informatique - 21158 - IFT 4006 - Z3 à 18:30 - 21:20
Conflit avec Spécification formelle et vérification de logiciels - 15442 - GLO 3004 - Z3 à 18:30 - 21:20
Conflit avec Gestion de projets informatiques : méthodes et outils - 21159 - GLO 3101 - Z3 à 18:30 - 21:20
```

## Format attendu des arguments
- Plage horaire (-t) : Doit être au format HH:MM - HH:MM.
- Jour de la semaine (-w) :
    - L : Lundi
    - M : Mardi
    - R : Mercredi
    - J : Jeudi
    - V : Vendredi
- Semestre (-s) :
    - 1 : Hiver
    - 3 : Été
    - 9 : Automne