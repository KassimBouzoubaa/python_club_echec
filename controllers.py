"""Définition des controllers"""
from dataclasses import dataclass
from typing import List, Optional

from models import Joueur, Match, Tour, Tournoi
from views import View
import random
from datetime import datetime


main_menu_choices = [
    "Tournois en cours",
    "Liste des tournois",
    "Liste des joueurs",
    "Rapports",
    "Sortir",
]


@dataclass
class ControllerState:
    joueurs: List[Joueur]
    tournois: List[Tournoi]
    tournois_en_cour: Optional[Tournoi] = None


class Controller:
    """Implémentation du controller"""

    def __init__(self, view: View):
        """Contient un tournoi et une view"""
        self.view = view
        self.state = ControllerState([], [])

    def menu_selection(self):
        choice = self.view.display_menu(main_menu_choices)
        if choice == 1:
            self.demarrer_tournoi()
            self.ajouter_joueur()
            print(self.state.tournois_en_cour)
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            pass
        elif choice == 5:
            print("Au revoir !")


    def demarrer_tournoi(self):
        champs_tournoi = ["nom", "lieu", "description"]
        input_tournoi = self.view.prompt_pour_tournoi(champs_tournoi)
        nom = input_tournoi["nom"]
        lieu = input_tournoi["lieu"]
        description = input_tournoi["description"]
        tournoi = Tournoi(nom, lieu, datetime.now().date(), description=description)
        self.state.tournois_en_cour = tournoi
        self.state.tournois_en_cour.init_tournoi()

    def ajouter_joueur(self):
        champs_joueur = ["nom", "prenom", "date de naissance"]
        while len(self.state.tournois_en_cour.liste_de_joueur) < 8:
            input_joueurs = self.view.get_user_input(champs_joueur)
            nom = input_joueurs["nom"]
            prenom = input_joueurs["prenom"]
            date_de_naissance = input_joueurs["date de naissance"]
            joueur = Joueur(nom, prenom, date_de_naissance)

            self.state.tournois_en_cour.liste_de_joueur.append(joueur)

    def verification_score_identique(self):
        """Si plusieurs joueurs ont le même nombre de points, ils vont être séléctionné de manière aléatoire."""
        scores_vus = []
        score_present = False

        for joueur in self.tournoi.liste_de_joueur:
            score = joueur.score
            if score in scores_vus:
                random.shuffle(
                    self.tournoi.liste_de_joueur
                )  # Mélangez la liste de joueurs pour obtenir un ordre aléatoire
            else:
                scores_vus.append(score)
        if score_present:
            self.melanger_joueurs()

    def distribution_points(self):
        """Distribut les points en fonction des resultats"""
        for match in self.tournoi.liste_de_tour[self.tournoi.tour_actuel - 1]:
            resultat = self.view.prompt_resultat()
            if resultat == "J1":
                """joueur1 = match[0][0]
                score joueur1 = match[0][1]
                joueur2 = match[1][0]
                score joueur2 = match[1][1]"""
                match.joueur[0].score += 1
                match.joueur[1].score -= 1
            elif resultat == "J2":
                match.joueur[0].score -= 1
                match.joueur[1].score += 1
            elif resultat == "N":
                match.joueur[0].score += 0.5
                match.joueur[1].score += 0.5

    def execution(self):
        """Execute le script principal du tournoi"""

        self.menu_selection()
        self.demarrer_tournoi()
        self.ajouter_joueur()
        self.melanger_joueurs()
        for i in range(0, self.tournoi.nombre_de_tours):
            self.tournoi.tour_actuel += 1
            self.generation_des_paires()
            self.distribution_points()
            self.tournoi.liste_de_tour[
                self.tournoi.tour_actuel - 1
            ].date_de_fin = datetime.now().date()
        self.tournoi.date_de_fin = datetime.now().date()


