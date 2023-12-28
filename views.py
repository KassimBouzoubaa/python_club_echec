from typing import List, Dict


class View:
    """Implémentation de la view."""

    def display_menu(self, choices: List[str], message: str) -> int:
        """Prompt du menu principal"""
        print(message)
        for index, choice in enumerate(choices):
            print(f"{index +1}. {choice}")
        while True:
            try:
                choice = int(input("Sélectionnez une option : "))
                if 1 <= choice <= len(choices):
                    return choice
                else:
                    print(
                        "Choix invalide. Veuillez entrez un nombre"
                        " entre 1 et ",
                        len(choices),
                    )
            except ValueError:
                print("Saisie invalide. Veuillez entrer un nombre.")

    def get_user_input(self, champs: List[str], message: str) ->\
            Dict[str, str]:
        """Prompt pour ajouter des joueurs"""
        print(message)
        inputs = {}
        for champ in champs:
            while True:
                valeur = input(f"Entrez {champ} : ")
                if valeur.strip():  # Vérifie que la valeur n'est pas
                    # vide ou composée uniquement d'espaces
                    inputs[champ] = valeur
                    break
                else:
                    print(f"Le champ {champ} ne peut pas être vide.")
        return inputs

    def simple_log(self, message: any):
        print(message)
