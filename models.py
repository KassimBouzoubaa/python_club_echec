"""Définition des models"""

from dataclasses import dataclass
from datetime import date


@dataclass
class Tournoi:
    """Définition d'un tournoi"""

    nom: str
    lieu: str
    date_de_debut: date
    liste_de_tour: list  # Liste de [Tour]
    liste_de_joueur: list  # Liste de [Joueur]
    description_remarque: str
    nombre_de_tours: int = 4
    tour_actuel: int = 0
    date_de_fin: date = None


@dataclass
class Tour:
    """Définition d'un tour"""

    tour: list  # Liste de [Match]
    name: str
    date_de_debut: date
    date_de_fin: date = None


@dataclass
class Match:
    """Définition d'un match"""

    participants: tuple  # Liste de [Joueur]


@dataclass
class Joueur:
    """Définition d'un joueur"""

    nom: str
    prenom: str
    date_de_naissance: str
    score: int = 0
