"""Définition des controllers"""

from models import Joueur, Match, Tour, Tournoi
from views import View
import random
from datetime import datetime


class Controller:
    """Implémentation du controller"""

    def __init__(self, view: View, tournoi: Tournoi):
        """Contient un tournoi et une view"""
        self.view = view
        self.tournoi = tournoi

    def demarrer_tournoi(self):
        nom, lieu, description = self.view.prompt_pour_tournoi()
        self.tournoi = Tournoi(
            nom, lieu, datetime.now().date(), [], [], description_remarque=description
        )

    def ajouter_joueur(self):
        while len(self.tournoi.liste_de_joueur) < 8:  # nombre de joueur maximum
            nom, prenom, date_de_naissance = self.view.prompt_pour_joueur()
            joueur = Joueur(nom, prenom, date_de_naissance)
            self.tournoi.liste_de_joueur.append(joueur)

    def melanger_joueurs(self):
        """Melanger les joueurs de manère aléatoire"""
        random.shuffle(self.tournoi.liste_de_joueur)

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

    def generation_des_paires(self):
        """Generation de paire pour un tour."""
        self.tournoi.liste_de_joueur.sort(key=lambda joueur: joueur.score, reverse=True)

        matchs = []
        self.verification_score_identique()

        for i in range(0, len(self.tournoi.liste_de_joueur), 2):
            joueur1 = self.tournoi.liste_de_joueur[i]
            joueur2 = self.tournoi.liste_de_joueur[i + 1]

            while (joueur1, joueur2) in matchs or (joueur2, joueur1) in matchs:
                joueur1 = self.tournoi.liste_de_joueur[i]
                joueur2 = self.tournoi.liste_de_joueur[i + 1]

            match = Match(([joueur1, joueur1.score], [joueur2, joueur2.score]))
            matchs.append(match)

        tour = Tour(matchs, f"Round ${self.tournoi.tour_actuel}", datetime.now().date())

        self.tournoi.liste_de_tour.append(tour)

    def distribution_points(self):
        """Distribut les points en fonction des resultats"""
        for match in self.tournoi.liste_de_tour[self.tournoi.tour_actuel - 1]:
            resultat = self.view.prompt_resultat()
            if resultat == "J1":
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
        self.demarrer_tournoi()
        self.ajouter_joueur()
        for i in range(0, self.tournoi.nombre_de_tours):
            self.tournoi.tour_actuel += 1
            self.generation_des_paires()
            self.distribution_points()
            self.tournoi.liste_de_tour[
                self.tournoi.tour_actuel - 1
            ].date_de_fin = datetime.now().date()
        self.tournoi.date_de_fin = datetime.now().date()
