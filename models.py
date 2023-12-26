"""Définition des models"""
from dataclasses import dataclass, field
from datetime import date, datetime
import random
from typing import List, Dict, Optional, Union, Tuple
import uuid


@dataclass
class Joueur:
    """Définition d'un joueur"""

    nom: str
    prenom: str
    date_de_naissance: date
    score: float = 0
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "nom": self.nom,
            "prenom": self.prenom,
            "score": self.score,
            "date_de_naissance": self.date_de_naissance.isoformat(),
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, donnee):
        score = donnee.get("score", 0)
        return Joueur(
            nom=donnee["nom"],
            prenom=donnee["prenom"],
            score=score,
            date_de_naissance=date.fromisoformat(donnee["date_de_naissance"]),
            id=donnee["id"],
        )


"""Définition d'un match"""
Match = Tuple[List[Union[Joueur, float]], List[Union[Joueur, float]]]


@dataclass
class Tour:
    """Définition d'un tour"""

    tour: List[Match]
    name: str
    date_de_debut: date =  datetime.now().date()
    date_de_fin: Optional[date] = None

    def to_dict(self):
        matchs_serializes = []
        for match in self.tour:
            donnees_joueur_1, donnees_joueur_2 = match
            match_serialize = [
                [donnees_joueur_1[0].id, donnees_joueur_1[1]],
                [donnees_joueur_2[0].id, donnees_joueur_2[1]],
            ]
            matchs_serializes.append(match_serialize)
        return {
            "tour": matchs_serializes,
            "name": self.name,
            "date_de_debut": self.date_de_debut.isoformat(),
            "date_de_fin": self.date_de_fin.isoformat()
            if self.date_de_fin is not None
            else None,
        }

    @classmethod
    def from_dict(cls, donnee, joueurs_par_id: Dict[str, Joueur]):
        matchs = []
        for donnee_match in donnee["tour"]:
            id_joueur_1, score_joueur_1 = donnee_match[0]
            id_joueur_2, score_joueur_2 = donnee_match[1]

            joueur1: Joueur = joueurs_par_id[id_joueur_1]
            joueur2: Joueur = joueurs_par_id[id_joueur_2]

            match = ([joueur1, score_joueur_1], [joueur2, score_joueur_2])
            matchs.append(match)

        return Tour(
            tour=matchs,
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
    description: str
    nombre_de_tours: int = 4
    tour_actuel: int = 0
    score_par_joueur: Dict[str, float] = field(default_factory=lambda: {})
    liste_de_tour: List[Tour] = field(default_factory=lambda: [])
    liste_de_joueur: List[Joueur] = field(default_factory=lambda: [])
    date_de_debut: Optional[date] = None
    date_de_fin: Optional[date] = None
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self):
        return {
            "nom": self.nom,
            "lieu": self.lieu,
            "description": self.description,
            "nombre_de_tours": self.nombre_de_tours,
            "tour_actuel": self.tour_actuel,
            "score_par_joueur": self.score_par_joueur,
            "liste_de_tour": [tour.to_dict() for tour in self.liste_de_tour],
            "liste_de_joueur": [joueur.to_dict() for joueur in self.liste_de_joueur],
            "date_de_debut": self.date_de_debut.isoformat()
            if self.date_de_debut is not None
            else None,
            "date_de_fin": self.date_de_fin.isoformat()
            if self.date_de_fin is not None
            else None,
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, donnee, joueurs, joueurs_dict):

        return Tournoi(
            nom=donnee["nom"],
            lieu=donnee["lieu"],
            description=donnee["description"],
            nombre_de_tours=donnee["nombre_de_tours"],
            tour_actuel=donnee["tour_actuel"],
            score_par_joueur=donnee["score_par_joueur"],
            liste_de_tour=[
                Tour.from_dict(tour, joueurs_dict) for tour in donnee["liste_de_tour"]
            ],
            liste_de_joueur=joueurs,
            date_de_debut=date.fromisoformat(donnee["date_de_debut"])
            if donnee["date_de_debut"] is not None
            else None,
            date_de_fin=date.fromisoformat(donnee["date_de_fin"])
            if donnee["date_de_fin"] is not None
            else None,
            id=donnee["id"],
        )

    def generation_de_paire(self) -> List[Match]:
        """Génération de paires de match"""

        joueurs = self.melanger_joueurs()

        if self.tour_actuel == 1:
            for joueur in joueurs:
                self.score_par_joueur[joueur.id] = 0

        matchs = []

        while len(joueurs) >= 2:  # Tant qu'il reste au moins deux joueurs
            joueur1 = joueurs.pop(0)  # Retire le premier joueur de la liste
            score_joueur1 = self.score_par_joueur[joueur1.id]

            print(joueur1)

            index = 0
            joueur2_trouve = False
            joueur2 = None
            score_joueur2 = None

            while index < len(joueurs):
                if not self.match_existe_deja(joueur1, joueurs[index]):
                    joueur2 = joueurs.pop(
                        index
                    )  # Utilise le joueur trouvé comme joueur 2
                    score_joueur2 = self.score_par_joueur[joueur2.id]
                    joueur2_trouve = True
                    break
                index += 1  # Passe au joueur suivant dans la liste

            # Création de la paire de joueurs avec leurs scores
            print("joueur2")
            match = ([joueur1, score_joueur1], [joueur2, score_joueur2])
            matchs.append(match)

        return matchs

    def generer_tour(self):
        matchs = self.generation_de_paire()
        print('match', matchs)
        tour = Tour(matchs, f"Round {self.tour_actuel}")
        self.liste_de_tour.append(tour)

    def demarrer(self):
        if self.tour_actuel == 0:
            self.tour_actuel += 1
            self.date_de_debut = datetime.now().date()
            self.generer_tour()

    def match_existe_deja(self, joueur1, joueur2):
        for tour in self.liste_de_tour:
            for match in tour.tour:
                # Comparaison des joueurs de chaque match avec le nouveau match
                if (
                    joueur1 == match[0][0]
                    and joueur2 == match[1][0]
                    or joueur1 == match[1][0]
                    and joueur2 == match[0][0]
                ):
                    return True  # Le match existe déjà
        return False

    def melanger_joueurs(self):
        joueurs_tries = self.liste_de_joueur[:]
        if self.tour_actuel == 1:
            random.shuffle(joueurs_tries)
        else:
            joueurs_tries = sorted(
                self.liste_de_joueur,
                key=lambda joueur: self.score_par_joueur.get(joueur.id, 0),
                reverse=True,  # Tri décroissant pour le score le plus élevé en premier
            )

        return joueurs_tries

    def passer_tour_suivant(self):
        self.liste_de_tour[self.tour_actuel - 1].date_de_fin = datetime.now().date()
        self.tour_actuel += 1
        self.generer_tour()

    def terminer(self):
        self.date_de_fin = datetime.now().date()
