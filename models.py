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
    date_de_naissance: date
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "date_de_naissance": self.date_de_naissance.isoformat(),
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, donnee):
        return Joueur(
            nom=donnee["nom"],
            prenom=donnee["prenom"],
            date_de_naissance=date.fromisoformat(donnee["date_de_naissance"]),
            id=donnee["id"],
        )


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
            "tour": self.tour,  # Implémenter
            "name": self.name,
            "date_de_debut": self.date_de_debut.isoformat(),
            "date_de_fin": self.date_de_fin.isoformat()
            if self.date_de_fin is not None
            else None,
        }

    @classmethod
    def from_dict(cls, donnee):
        return Tour(
            tour=donnee["tour"],
            name=donnee["name"],
            date_de_debut=date.fromisoformat(donnee["date_de_debut"]),
            date_de_fin=date.fromisoformat(donnee["date_de_fin"])
            if donnee["date_de_fin"] is not None
            else None,
        )


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
            "date_de_debut": self.date_de_debut.isoformat(),
            "description": self.description,
            "nombre_de_tours": self.nombre_de_tours,
            "tour_actuel": self.tour_actuel,
            "score_par_joueur": self.score_par_joueur,
            "liste_de_tour": self.liste_de_tour,
            "liste_de_joueur": self.liste_de_joueur,
            "date_de_fin": self.date_de_fin,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, donnee):
        return Tournoi(
            nom=donnee["nom"],
            lieu=donnee["lieu"],
            date_de_debut=date.fromisoformat(donnee["date_de_debut"]),
            description=donnee["description"],
            nombre_de_tours=donnee["nombre_de_tours"],
            tour_actuel=donnee["tour_actuel"],
            score_par_joueur=donnee["score_par_joueur"],
            liste_de_tour=donnee["liste_de_tour"],
            liste_de_joueur=donnee["liste_de_joueur"],
            date_de_fin=date.fromisoformat(donnee["date_de_fin"])
            if donnee["date_de_fin"] is not None
            else None,
            id=donnee["id"],
        )
