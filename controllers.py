"""Définition des controllers"""
from dataclasses import dataclass, field
from operator import attrgetter
from typing import List, Optional, Dict
import json

from models import Joueur, Tournoi
from views import View
from datetime import datetime, date

main_menu_choices = [
    "Tournois en cours",
    "Liste des tournois",
    "Liste des joueurs",
    "Rapports",
    "Sortir",
]


@dataclass
class ControllerState:
    joueurs: Dict[str, Joueur] = field(default_factory=lambda: dict())
    tournois: Dict[str, Tournoi] = field(default_factory=lambda: dict())
    tournoi_en_cours: Optional[Tournoi] = None

    @classmethod
    def from_json(cls, filepath: str):
        """Sérialise les information de mon state (joueurs, tournois, tournoi_en_cours
        pour les récupérer du JSON sous la forme d'un dictionnaire avec les ids
        en clé et les objets en valeur.
        """
        with open(filepath, "r") as f:
            donnees = json.load(f)

        joueurs = [Joueur.from_dict(data) for data in donnees["liste_de_joueurs"]]
        joueurs_dict = {joueur.id: joueur for joueur in joueurs}

        tournois = [
            Tournoi.from_dict(data,joueurs)
            for data in donnees["liste_de_tournoi"]
        ]
        tournois_dict = {tournoi.id: tournoi for tournoi in tournois}

        tournoi_en_cours = tournois_dict.get(
            donnees["tournoi_en_cours"]
        ) if donnees and donnees["tournoi_en_cours"] is not None else None

        return ControllerState(
            joueurs=joueurs_dict,
            tournois=tournois_dict,
            tournoi_en_cours=tournoi_en_cours,
        )

    def to_json(self, filepath: str):
        """Sérialise les information de mon state (joueurs, tournois)
        pour les enregistrer dans le JSON en tant que liste de dictionnaire.
        """
        joueurs_serialized = [joueur.to_dict() for joueur in self.joueurs.values()]
        tournois_serialized = [tournoi.to_dict() for tournoi in self.tournois.values()]
        tournoi_en_cours = (
            self.tournoi_en_cours.to_dict()
            if self.tournoi_en_cours is not None
            else None
        )

        donnees = {
            "liste_de_joueurs": joueurs_serialized,
            "liste_de_tournoi": tournois_serialized,
            "tournoi_en_cours": tournoi_en_cours,
        }
        try:
            with open(filepath, "w") as f:
                json.dump(donnees, f, indent=4)
        except Exception as e:
            print("Une erreur s'est produite lors de la sauvegarde des données :", e)


class Controller:
    """Implémentation du controller"""

    JSON_DB_FILEPATH = "data/tournaments.json"

    def __init__(self, view: View):
        """Contient un tournoi et une view"""
        self.view = view
        self.state = ControllerState.from_json(self.JSON_DB_FILEPATH)

    # ----------------------------
    # Menu functions
    # ----------------------------

    def menu_principal(self):
        """Menu principal"""

        choice = self.view.display_menu(main_menu_choices, "Menu principal")
        if choice == 1:
            self.menu_tournoi_en_cours()
        elif choice == 2:
            self.menu_liste_des_tournois()
        elif choice == 3:
            self.menu_liste_des_joueurs()
        elif choice == 4:
            self.menu_rapports()
        elif choice == 5:
            self.exit()

        self.save()

    def menu_tournoi_en_cours(self):
        """Menu du tournoi en cour"""

        if self.state.tournoi_en_cours is None:
            self.choisir_tournoi_en_cours()
            self.menu_tournoi_en_cours()
        else:
            if self.state.tournoi_en_cours.tour_actuel == 0:
                choice = self.view.display_menu(
                    ["Démarrer le tournoi", "Ajouter des joueurs", "Retour"],
                    "Menu du tournoi en cour",
                )
                if choice == 1:
                    self.state.tournoi_en_cours.demarrer()
                    self.menu_tournoi_en_cours()
                elif choice == 2:
                    self.ajouter_joueur_tournoi()
                    self.menu_tournoi_en_cours()
                else:
                    self.menu_principal()
            else:
                choice = self.view.display_menu(
                    [
                        "Entrer les résultats du tour",
                        "Passer au tour suivant",
                        "Finir le tournoi",
                        "Retour",
                    ],
                    "Tournoi en cour",
                )
                if choice == 1:
                    self.entrer_resultats_du_tour()
                    self.menu_tournoi_en_cours()
                elif choice == 2:
                    self.state.tournoi_en_cours.passer_tour_suivant()
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
            ],
            "Menu liste des tournois",
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
            ],
            "Menu liste des joueurs",
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

        choice = self.view.display_menu(
            [
                "Liste des joueurs par ordre alphabétique",
                "Liste de tout les tournois",
                "Nom et date d'un tournoi donné",
                "Liste des joueurs d'un tournoi par ordre alphabétique",
                "Liste de tous les tours du tournoi et de tous les matchs du tour",
                "Retour",
            ],
            "Menu rapport",
        )
        if choice == 1:
            self.liste_joueurs_trier()
            self.menu_rapports()
        elif choice == 2:
            self.liste_tournoi()
            self.menu_rapports()
        elif choice == 3:
            self.get_tournoi()
            self.menu_rapports()
        elif choice == 4:
            self.get_joueurs_par_tournoi()
            self.menu_rapports()
        elif choice == 5:
            self.get_tours_matchs_par_tournoi()
            self.menu_rapports()
        elif choice == 6:
            self.menu_principal()

    # ----------------------------
    # Tournoi functions
    # ----------------------------

    def choisir_tournoi_en_cours(self):
        """Selection du tournoi en cour"""

        message = "Selectionnez l'id du tournoi:\n" + "\n".join(
            [
                f"{tournoi.nom} (id: {tournoi.id})"
                for tournoi in self.state.tournois.values()
            ]
        )
        tournoi = None
        while tournoi is None:
            id_tournoi = self.view.get_user_input(["Id du tournoi"], message=message)
            id = id_tournoi["Id du tournoi"]

            tournoi = self.state.tournois.get(id)

        self.state.tournoi_en_cours = tournoi
        self.save()

    def entrer_resultats_du_tour(self):
        """Récupération des résultats"""
        for match in self.state.tournoi_en_cours.liste_de_tour[
            self.state.tournoi_en_cours.tour_actuel
        ].tour:
            message = "Quel est le resultat du match"
            champ_resultat = ["joueur1, joueur2, nul"]
            input_resultat = self.view.display_menu(champ_resultat, message)
            if input_resultat == 1:
                self.state.tournoi_en_cours.score_par_joueur[match[0][0].id] += 1
            elif input_resultat == 2:
                self.state.tournoi_en_cours.score_par_joueur[match[1][0].id] += 1
            elif input_resultat == 3:
                self.state.tournoi_en_cours.score_par_joueur[match[0][0].id] += 0.5
                self.state.tournoi_en_cours.score_par_joueur[match[1][0].id] += 0.5

        self.save()

    def terminer_tournoi(self):
        """Terminer le tournoi en cours"""

        self.state.tournoi_en_cours.terminer()
        for joueur in self.state.tournoi_en_cours.liste_de_joueur:
            joueur.score += self.state.tournoi_en_cours.score_par_joueur[joueur.id]
        self.state.tournois[
            self.state.tournoi_en_cours.id
        ] = self.state.tournoi_en_cours
        self.state.tournoi_en_cours = None
        self.save()

    def creation_tournoi(self):
        """Création d'un tournoi"""

        message = "Creation du tournoi"
        champs_tournoi = ["nom", "lieu", "description"]
        input_tournoi = self.view.get_user_input(champs_tournoi, message)
        tournoi = Tournoi(
            input_tournoi["nom"],
            input_tournoi["lieu"],
            description=input_tournoi["description"],
        )
        self.state.tournois[tournoi.id] = tournoi
        self.save()

    def modifier_tournoi(self):
        """Modifie un tournoi"""
        message = "Sélectionnez l'id du tournoi :\n" + "\n".join(
            [
                f"{tournoi.nom} (id: {tournoi.id})"
                for tournoi in self.state.tournois.values()
            ]
        )

        id_tournoi = None
        while id_tournoi is None:
            id_input = self.view.get_user_input(["Id du tournoi"], message=message)
            id_tournoi = id_input["Id du tournoi"]
            if id_tournoi not in [
                tournoi.id for tournoi in self.state.tournois.values()
            ]:
                self.view.simple_log("L'id du tournoi n'existe pas, veuillez ressayer.")
                return

        champs = ["nom, lieu ou description"]

        valeur_champ = self.view.get_user_input(champs, "Que souhaitez-vous modifier ?")
        champ = valeur_champ["nom, lieu ou description"]
        if champ not in ["nom", "lieu", "description"]:
            self.view.simple_log(
                "Erreur de format. Assurez-vous d'entrer la valeur correctement."
            )
            return

        valeur = self.view.get_user_input(
            [champ], f"Entrez la nouvelle valeur pour {champ.capitalize()}"
        )

        for tournoi in self.state.tournois.values():
            if tournoi.id == id_tournoi:
                if champ == "nom":
                    tournoi.nom = valeur[champ]
                elif champ == "lieu":
                    tournoi.lieu = valeur[champ]
                elif champ == "description":
                    tournoi.description = valeur[champ]

        self.save()

    def liste_tournoi(self):
        """Liste des tournois"""

        self.view.simple_log("Liste des tournois : ")
        for tournoi in self.state.tournois.values():
            self.view.simple_log(tournoi.nom)

    def get_tournoi(self):
        """Récupère le nom et la date d'un tournoi donné"""

        message = "Selectionnez l'id du tournoi:\n" + "\n".join(
            [
                f"{tournoi.nom} (id: {tournoi.id})"
                for tournoi in self.state.tournois.values()
            ]
        )
        tournoi = None
        while tournoi is None:
            id_tournoi = self.view.get_user_input(["Id du tournoi"], message=message)
            id = id_tournoi["Id du tournoi"]

            tournoi = self.state.tournois.get(id)

        self.view.simple_log(
            f"nom: {tournoi.nom}\ndate de debut: {tournoi.date_de_debut}\ndate de fin: {tournoi.date_de_fin}"
        )

    def get_joueurs_par_tournoi(self):
        """Récupère la liste des joueurs d'un tournoi par ordre alphabétique"""

        message = "Selectionnez l'id du tournoi:\n" + "\n".join(
            [
                f"{tournoi.nom} (id: {tournoi.id})"
                for tournoi in self.state.tournois.values()
            ]
        )
        tournoi = None
        while tournoi is None:
            id_tournoi = self.view.get_user_input(["Id du tournoi"], message=message)
            id = id_tournoi["Id du tournoi"]
            tournoi = self.state.tournois.get(id)

        joueurs_tries = sorted(tournoi.liste_de_joueur, key=attrgetter("nom"))

        self.view.simple_log("Liste des joueurs : ")
        for joueur in joueurs_tries:
            self.view.simple_log(joueur.to_dict())

    def get_tours_matchs_par_tournoi(self):
        """Récupère les tours et les matchs d'un tournoi"""

        message = "Selectionnez l'id du tournoi:\n" + "\n".join(
            [
                f"{tournoi.nom} (id: {tournoi.id})"
                for tournoi in self.state.tournois.values()
            ]
        )
        tournoi = None
        while tournoi is None:
            id_tournoi = self.view.get_user_input(["Id du tournoi"], message=message)
            id = id_tournoi["Id du tournoi"]
            tournoi = self.state.tournois.get(id)

        self.view.simple_log("Liste des tours : ")

        for tour in tournoi.liste_de_tour:
            self.view.simple_log(tour.name)
            self.view.simple_log(tour)
            self.view.simple_log("Liste des matchs")
            for match in tour.tour:
                self.view.simple_log(match)

    # ----------------------------
    # Joueurs functions
    # ----------------------------

    def ajouter_joueur(self):
        """Ajouter des joueurs"""

        message = "Ajout d'un joueur"
        champs_joueur = ["nom", "prenom", "date de naissance (YYYY-MM-DD)"]

        valeurs_joueur = self.view.get_user_input(champs_joueur, message)
        try:
            date_de_naissance = date.fromisoformat(
                valeurs_joueur["date de naissance (YYYY-MM-DD)"]
            )
            joueur = Joueur(
                valeurs_joueur["nom"], valeurs_joueur["prenom"], date_de_naissance
            )

            self.state.joueurs[joueur.id] = joueur

        except ValueError:
            self.view.simple_log(
                "Erreur de format. Assurez-vous d'entrer la valeur correctement."
            )

            self.ajouter_joueur()
            self.save()

    def ajouter_joueur_tournoi(self):
        "Ajouter des joueurs au tournoi en cours"

        message = "Selectionnez l'id du joueur:\n" + "\n".join(
            [
                f"{joueur.nom} (id: {joueur.id})"
                for joueur in self.state.joueurs.values()
            ]
        )
        id = None
        while id is None:
            id_joueur = self.view.get_user_input(["Id du joueur"], message=message)
            id = id_joueur["Id du joueur"]

            for joueur in self.state.joueurs.values():
                if joueur.id == id:
                    self.state.tournoi_en_cours.liste_de_joueur.append(joueur)

        self.view.simple_log("Le joueur à bien été ajouté au tournoi en cour.")
        self.save()

    def modifier_joueur(self):
        """Modifie un joueur"""
        message = "Sélectionnez l'id du joueur :\n" + "\n".join(
            [
                f"{joueur.nom} (id: {joueur.id})"
                for joueur in self.state.joueurs.values()
            ]
        )

        id_joueur = None
        while id_joueur is None:
            id_input = self.view.get_user_input(["Id du joueur"], message=message)
            id_joueur = id_input["Id du joueur"]

        champs = ["nom, prenom ou date de naissance"]
        valeur_champ = self.view.get_user_input(champs, "Que souhaitez-vous modifier ?")
        champ = valeur_champ["nom, prenom ou date de naissance"]
        valeur = self.view.get_user_input(
            [champ], f"Entrez la nouvelle valeur pour {champ.capitalize()}"
        )

        for joueur in self.state.joueurs.values():
            if joueur.id == id_joueur:
                if champ == "nom":
                    joueur.nom = valeur[champ]
                elif champ == "prenom":
                    joueur.prenom = valeur[champ]
                elif champ == "date de naissance":
                    joueur.date_de_naissance = valeur[champ]

        self.save()

    def lister_les_joueurs(self):
        """Liste tout les joueurs"""

        self.view.simple_log("Liste des joueurs : ")

        for joueur in self.state.joueurs.values():
            self.view.simple_log(joueur.to_dict())

    def liste_joueurs_trier(self):
        """Récupère tout les joueurs et les tri par ordre alphabétique"""

        joueurs_tries = sorted(self.state.joueurs.values(), key=attrgetter("nom"))

        self.view.simple_log("Liste des joueurs : ")
        for joueur in joueurs_tries:
            self.view.simple_log(joueur.to_dict())

    # ----------------------------
    # Others functions
    # ----------------------------

    def save(self):
        self.state.to_json(self.JSON_DB_FILEPATH)

    def exit(self):
        """Termine la session"""

        self.view.simple_log("Session terminée.")
