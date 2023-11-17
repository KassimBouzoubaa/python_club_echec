"""Définition des controllers"""
from dataclasses import dataclass, field
from typing import List, Optional
import json

from models import Joueur, Tournoi
from views import View
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
    tournoi_en_cours: Optional[Tournoi] = None


class Controller:
    """Implémentation du controller"""

    def __init__(self, view: View):
        """Contient un tournoi et une view"""
        self.view = view
        self.state = ControllerState()

    # ----------------------------
    # Menu functions
    # ----------------------------

    def menu_principal(self):
        """Menu principal"""

        choice = self.view.display_menu(main_menu_choices)
        if choice == 1:
            self.menu_tournoi_en_cours()
        elif choice == 2:
            self.menu_liste_des_tournois()
        elif choice == 3:
            self.menu_liste_des_joueurs()
        elif choice == 4:
            self.menu_rapports()
        elif choice == 5:
            self.exit()  # Implémenter

    def menu_tournoi_en_cours(self):
        """Menu du tournoi en cour"""

        if self.state.tournoi_en_cours == None:
            self.choisir_tournoi_en_cours()
            self.menu_tournoi_en_cours()
        else:
            # est-ce que mon tournoi est démarré?
            if self.state.tournoi_en_cours.tour_actuel == 0:
                choice = self.view.display_menu(
                    ["Démarrer le tournoi", "Ajouter des joueurs", "Retour"]
                )
                if choice == 1:
                    self.demarrer_tournoi_en_cours()
                    self.menu_tournoi_en_cours()
                elif choice == 2:
                    self.ajouter_joueur()
                    self.menu_tournoi_en_cours()
                else:
                    self.menu_principal()
            else:
                choice = self.view.display_menu(
                    [
                        "Entrer les résultats du tour",
                        "Passer au tour suivant",
                        "Finir le tournoi" "Retour",
                    ]
                )
                if choice == 1:
                    self.entrer_resultats_du_tour()
                    self.menu_tournoi_en_cours()
                elif choice == 2:
                    self.passer_au_tour_suivant()
                    self.menu_tournoi_en_cours()
                elif choice == 3:
                    self.terminer_tournoi()
                    self.menu_principal()
                else:
                    self.menu_principal()

    def menu_liste_des_tournois(self):
        """Menu liste des tournois"""

        choice = self.view.display_menu(
            [
                "Ajouter un tournoi",
                "Modifier un tournoi",
                "Lister les tournois",
                "Retour",
            ]
        )
        if choice == 1:
            self.creation_tournoi()
            self.menu_liste_des_tournois()
        elif choice == 2:
            self.modifier_tournoi()
            self.menu_liste_des_tournois()
        elif choice == 3:
            self.liste_tournoi()
            self.menu_liste_des_tournois()
        elif choice == 4:
            self.menu_principal()

    def menu_liste_des_joueurs(self):
        """Menu liste des joueurs"""

        choice = self.view.display_menu(
            [
                "Ajouter des joueurs",
                "Modifier des joueurs",
                "Lister les joueurs",
                "Retour",
            ]
        )
        if choice == 1:
            self.ajouter_joueur()
            self.menu_liste_des_joueurs()
        elif choice == 2:
            self.modifier_joueur()
            self.menu_liste_des_joueurs()
        elif choice == 3:
            self.lister_les_joueurs()
            self.menu_liste_des_joueurs()
        elif choice == 4:
            self.menu_principal()

    def menu_rapports(self):
        """Menu rapport"""

        pass

    # ----------------------------
    # Tournoi functions
    # ----------------------------

    def choisir_tournoi_en_cours(self):
        """Selection du tournoi en cour"""

        message = "Selectionnez l'id du tournoi:\n" + "\n".join(
            [f"{tournoi.nom} (id: {tournoi.id})" for tournoi in self.state.tournois]
        )
        tournoi = None
        while tournoi is None:
            id_tournoi = self.view.get_user_input(["Id du tournoi"], message=message)
            tournois_par_id = {tournoi.id: tournoi for tournoi in self.state.tournois}
            tournoi = tournois_par_id.get(id_tournoi)  # A comprendre

        self.state.tournoi_en_cours = tournoi

    def demarrer_tournoi_en_cours(self):
        pass

    def entrer_resultats_du_tour(self):
        pass

    def passer_au_tour_suivant(self):
        pass

    def terminer_tournoi(self):
        """Terminer le tournoi en cours"""

        self.state.tournoi_en_cours.date_de_fin = datetime.now().date()
        donnees["liste_de_tournoi"].append(self.state.tournoi_en_cours.to_dict())

    def creation_tournoi(self):
        """Création d'un tournoi"""

        message = "Creation du tournoi"
        champs_tournoi = ["nom", "lieu", "description"]
        input_tournoi = self.view.get_user_input(champs_tournoi, message)
        tournoi = Tournoi(
            input_tournoi["nom"],
            input_tournoi["lieu"],
            datetime.now().date(),
            description=input_tournoi["description"]
        )
        self.state.tournois.append(tournoi.to_dict())

    def modifier_tournoi(self):
        pass

    def liste_tournoi(self):
        """Liste des tournois"""

        print("Liste des tournois : ")
        for tournoi in self.state.tournois:
            print(tournoi)

    # ----------------------------
    # Joueurs functions
    # ----------------------------

    def ajouter_joueur(self):
        """Ajouter des joueurs"""

        message = "Ajout d'un joueur"
        champs_joueur = ["nom", "prenom", "date de naissance"]

        valeurs_joueur = self.view.get_user_input(champs_joueur, message)
        joueur = Joueur(valeurs_joueur["nom"], valeurs_joueur["prenom"],  valeurs_joueur["date de naissance"])

        self.state.joueurs.append(joueur.to_dict())

    def modifier_joueur(self):
        pass

    def lister_les_joueurs(self):
        pass

    def liste_joueurs_trier(self):
        """Récupère tout les joueurs et les tri par ordre alphabétique"""

        joueurs_tries = sorted(self.state.joueurs, key=lambda joueur: joueur["nom"])
        print("Liste des joueurs : ")
        for joueur in joueurs_tries:
            print(joueur)

    # ----------------------------
    # Donnees functions
    # ----------------------------
    def sauvegarder_donnees(self):
        """Sauvegarde les données dans le dossier data"""

        try:
            with open("data/tournaments.json", "w") as f:
                json.dump(donnees, f, indent=4)
        except Exception as e:
            print("Une erreur s'est produite lors de la sauvegarde des données :", e)

    # ----------------------------
    # Others functions
    # ----------------------------

    def exit(self):
        """Termine la session"""

        print("Session terminée.")