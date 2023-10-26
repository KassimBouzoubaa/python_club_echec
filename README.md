# Logiciel de Gestion de Tournoi pour le Club d'Échecs

## Introduction

Ce logiciel de gestion de tournoi a été conçu pour aider notre club d'échecs à organiser et gérer efficacement des tournois d'échecs. Le logiciel fonctionne en mode hors ligne, ce qui signifie que vous pouvez l'utiliser même en l'absence d'une connexion Internet. Il permet de sauvegarder et de revoir les résultats des tournois de manière simple et efficace.

## Installation

Pour utiliser ce logiciel, veuillez suivre ces étapes d'installation :

1. Clonez le référentiel depuis GitHub :

   ```bash
   git clone https://github.com/KassimBouzoubaa/python_club_echec.git

2. Accédez au répertoire du projet :

   ```bash
   cd gestion-de-tournoi
3. Créez un environnement virtuel Python pour isoler les dépendances :

   ```bash
   python -m venv env
4. Activez l'environnement virtuel :
   
    ```bash
   source venv/bin/activate
5. Installez les dépendances requises :

   ```bash
   pip install -r requirements.txt
   
## Utilisation

Le logiciel de gestion de tournoi suit le modèle Modèle-Vue-Contrôleur (MVC) pour organiser les entités et les fonctionnalités du programme :

Modèles : Les classes modèles représentent les entités du programme, notamment les joueurs, les tournois, les matchs et les rondes. Ces classes sont responsables de la gestion des données.

Vues : Les vues sont responsables de l'affichage des informations, y compris les classements, les appariements et d'autres statistiques. Les vues fournissent une interface utilisateur conviviale.

Contrôleurs : Les contrôleurs gèrent les interactions de l'utilisateur, la saisie de données et la logique métier. Ils produisent les résultats des matchs, lancent de nouveaux tournois, etc.

L'utilisation du programme est conviviale et intuitive. Vous pourrez naviguer facilement entre les différentes fonctionnalités du logiciel.

## Conception du Programme

Le programme est basé sur le modèle Modèle-Vue-Contrôleur (MVC), ce qui permet une organisation claire et modulaire du code. Les fichiers de données sont stockés au format JSON pour assurer la portabilité et la facilité d'utilisation.

## Rapport de Linting
Nous utilisons Flake8 pour vérifier la qualité du code source. Assurez-vous que le code est exempt d'erreurs de linting en exécutant la commande suivante :

   ```bash
   flake8 --format=html --htmldir=flake8-report   
   ```
Le rapport de linting sera généré dans le répertoire flake8-report pour vous assurer que le code est conforme aux normes.