from datetime import date
from typing import List, Dict, Any

from models import Tournoi


class View:
    """Implémentation de la view."""

    def display_menu(self, choices: List[str]) -> int:
        """Prompt du menu principal"""
        print("Menu principal:")
        for index, choice in enumerate(choices):
            print(f"{index +1}. {choice}")
        while True:
            try:
                choice = int(input("Sélectionnez une option : "))
                if 1 <= choice <= len(choices):
                    return choice
                else:
                    print(
                        "Choix invalide. Veuillez entrez un nombre entre 1 et ",
                        len(choices),
                    )
            except ValueError:
                print("Saisie invalide. Veuillez entrer un nombre.")

    def get_user_input(self, champs: List[str]) -> Dict[str, str]:
        """Prompt pour ajouter des joueurs"""
        print("Création de joueur")
        input_joueurs = {}
        for champ in champs:
            while True:
                valeur = input(f"Entrez {champ} : ")
                if valeur.strip():  # Vérifie que la valeur n'est pas vide ou composée uniquement d'espaces
                    input_joueurs[champ] = valeur
                    break
                else:
                    print(f"Le champ {champ} ne peut pas être vide.")
        return input_joueurs

    def prompt_pour_creation_tournoi(self, champs: List[str]) -> Dict[str, str]:
        """Prompt pour créer le tournoi"""
        print("Creation du tournoi")
        input_tournoi = {}
        for champ in champs:
            input_tournoi[champ] = input(f"Entrez {champ} : ")
        return input_tournoi

    def prompt_pour_selectionner_tournoi(self, choices: List[Tournoi]) -> int:
        print("Selectionnez le tournoi")
        for index, choice in enumerate(choices):
            print(f"{index}. {choice.nom}")
        while True:
            try:
                choice = int(input("Sélectionnez une option : "))
                if 0 <= choice <= len(choices):
                    return choice
                else:
                    print(
                        "Choix invalide. Veuillez entrez un nombre entre 0 et ",
                        len(choices),
                    )
            except ValueError:
                print("Saisie invalide. Veuillez entrer un nombre.")

    def prompt_resultat(self):
        """Prompt pour déterminer les resultats"""
        resultat = input("Quel est le resultat? (J1 / J2 / N )")
        try:
            if resultat == "J1" or "J2" or "N":
                return resultat
            else:
                print("Choix invalide. Veuilliez entrer (J1 / J2 / N )")
        except ValueError:
            print("Saisie invalide")

    def menu_creation_tournoi(self, champs: List[str]) -> int:
        pass
