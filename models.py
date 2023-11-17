"""Définition des models"""
from dataclasses import dataclass, field
from datetime import date
from typing import List, Dict, Optional, Union, Tuple
import uuid


@dataclass
class Joueur:
    """Définition d'un joueur"""

    nom: str
    prenom: str
    date_de_naissance: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_de_naissance": self.date_de_naissance,
            "id": self.id
        }

"""Définition d'un match"""
Match = Tuple[List[Union[Joueur, int]], List[Union[Joueur, int]]]


@dataclass
class Tour:
    """Définition d'un tour"""

    tour: List[Match]
    name: str
    date_de_debut: date
    date_de_fin: Optional[date] = None

    def to_dict(self):
        return {
            "tour": self.tour,
            "name": self.name,
            "date_de_debut": self.date_de_debut.strftime("%Y-%m-%d"),
            "date_de_fin": self.date_de_fin
        }

@dataclass
class Tournoi:
    """Définition d'un tournoi"""

    nom: str
    lieu: str
    date_de_debut: date
    description: str
    nombre_de_tours: int = 4
    tour_actuel: int = 0
    score_par_joueur: Dict[str, int] = field(default_factory=lambda: {})
    liste_de_tour: List[Tour] = field(default_factory=lambda: [])
    liste_de_joueur: List[Joueur] = field(default_factory=lambda: [])
    date_de_fin: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "date_de_debut": self.date_de_debut.strftime("%Y-%m-%d"),
            "description": self.description,
            "nombre_de_tours": self.nombre_de_tours,
            "tour_actuel": self.tour_actuel,
            "score_par_joueur" : self.score_par_joueur,
            "liste_de_tour": self.liste_de_tour,
            "liste_de_joueur": self.liste_de_joueur,
            "date_de_fin": self.date_de_fin,
            "id": self.id
        }