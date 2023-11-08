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


"""Définition d'un match"""
Match = Tuple[List[Union[Joueur, int]], List[Union[Joueur, int]]]


@dataclass
class Tour:
    """Définition d'un tour"""

    tour: List[Match]
    name: str
    date_de_debut: date
    date_de_fin: Optional[date] = None


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

    def init_tournoi(self):
        self.score_par_joueur = {joueur.id: 0 for joueur in self.liste_de_joueur}
        """ def generation_des_paires(self):

        joueurs = []
        if self.tour_actuel == 1:
            joueurs = sorted(self.liste_de_joueur, key=lambda k: random.random() )
        else:
            joueurs = self.liste_de_joueur.sort(key=lambda joueur: self.score_par_joueur[joueur.id], reverse=True) #


        matchs = []
        self.verification_score_identique()

        for i in range(0, len(self.liste_de_joueur), 2):
            joueur1 = self.liste_de_joueur[i]
            joueur2 = self.liste_de_joueur[i + 1]

            while (joueur1, joueur2) in matchs or (joueur2, joueur1) in matchs:
                joueur1 = self.liste_de_joueur[i]
                joueur2 = self.liste_de_joueur[i + 1]

            match = Match(([joueur1, joueur1.score], [joueur2, joueur2.score]))  # A vérifier
            matchs.append(match)

        tour = Tour(matchs, f"Round ${self.tour_actuel}", datetime.now().date())

        self.liste_de_tour.append(tour)"""
