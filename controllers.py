"""Définition des controllers"""
from dataclasses import dataclass, field
from typing import List, Optional
import json

from models import Joueur, Match, Tour, Tournoi
from views import View
import random
from datetime import datetime

with open("data/tournaments.json", "r") as f:
    donnees = json.load(f)

main_menu_choices = [
    "Tournois en cours",
    "Liste des tournois",
    "Liste des joueurs",
    "Rapports",
    "Sortir",
]


@dataclass
class ControllerState:
    joueurs: List[Joueur] = field(default_factory=lambda: donnees["liste_de_joueurs"])
    tournois: List[Tournoi] = field(default_factory=lambda: donnees["liste_de_tournoi"])
    tournois_en_cour: Optional[Tournoi] = None


class Controller:
    """Implémentation du controller"""

    def __init__(self, view: View):
        """Contient un tournoi et une view"""
        self.view = view
        self.state = ControllerState()

    def menu_selection(self):
        choice = self.view.display_menu(main_menu_choices)
        if choice == 1:
            self.creation_tournoi()
        elif choice == 2:
            self.liste_tournoi()
        elif choice == 3:
            self.liste_joueurs_trier()
        elif choice == 4:
            pass
        elif choice == 5:
            print("Au revoir !")
        self.sauvegarder_donnees()

    def sauvegarder_donnees(self):
        try:
            with open("data/tournaments.json", "w") as f:
                json.dump(donnees, f, indent=4)
        except Exception as e:
            print("Une erreur s'est produite lors de la sauvegarde des données :", e)

    def creation_tournoi(self):
        champs_tournoi = ["nom", "lieu", "description"]
        input_tournoi = self.view.prompt_pour_creation_tournoi(champs_tournoi)
        nom = input_tournoi["nom"]
        lieu = input_tournoi["lieu"]
        description = input_tournoi["description"]
        tournoi = Tournoi(nom, lieu, datetime.now().date(), description=description)
        self.state.tournois.append(tournoi.to_dict())

    def selection_tournoi(self):
        choice = self.view.prompt_pour_selectionner_tournoi(self.state.tournois)
        self.state.tournois_en_cour = self.state.tournois[choice]

    def ajouter_joueur(self):
        champs_joueur = ["nom", "prenom", "date de naissance"]

        input_joueurs = self.view.get_user_input(champs_joueur)
        nom = input_joueurs["nom"]
        prenom = input_joueurs["prenom"]
        date_de_naissance = input_joueurs["date de naissance"]
        joueur = Joueur(nom, prenom, date_de_naissance)

        self.state.joueurs.append(joueur.to_dict())

    """
        def verification_score_identique(self):
            Si plusieurs joueurs ont le même nombre de points, ils vont être séléctionné de manière aléatoire.
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
            Distribut les points en fonction des resultats
            for match in self.state.tournois_en_cour.liste_de_tour[self.state.tournois_en_cour.tour_actuel - 1]:
                resultat = self.view.prompt_resultat()
                if resultat == "J1":
                    match[0][1] += 1
                    match[1][1] -= 1
                elif resultat == "J2":
                    match[0][1] -= 1
                    match[1][1] += 1
                elif resultat == "N":
                    match[0][1] += 0.5
                    match[1][1] += 0.5
    """

    def liste_joueurs_trier(self):
        """Récupère tout les joueurs et les tri par ordre alphabétique"""
        with open("data/tournaments.json", "r") as f:
            donnees = json.load(f)
        joueurs_tries = sorted(
            donnees["liste_de_joueurs"], key=lambda joueur: joueur["nom"]
        )
        print("Liste des joueurs : ")
        for joueur in joueurs_tries:
            print(joueur)

    def liste_tournoi(self):
        print("Liste des tournois : ")
        for tournoi in self.state.tournois:
            print(tournoi)
    def terminer_tournoi(self):
        self.state.tournois_en_cour.date_de_fin = datetime.now().date()
        donnees["liste_de_tournoi"].append(self.state.tournois_en_cour.to_dict())

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


con = Controller(view=View())
con.menu_selection()

