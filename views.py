from datetime import date


class View:
    """Implémentation de la view."""

    def prompt_pour_joueur(self):
        """Prompt ajouter un joueur."""
        nom = input("tapez le nom du joueur : ")
        prenom = input("tapez le prenom du joueur : ")
        date_str = input(
            "tapez la date de naissance du joueur (au format JJ/MM/AAAA) : "
        )
        date_de_naissance = date(*map(int, date_str.split("/")))

        if not nom or not prenom or not date_de_naissance:
            return None
        return nom, prenom, date_de_naissance

    def prompt_pour_tournoi(self):
        """Prompt pour démarer le tournoi"""
        nom = input("Entrez le nom du tournoi")
        lieu = input("Entrez le nom du lieu")
        description = input("Entrez les remarques générales du tournoi")

        if not nom or not lieu or not description:
            return None
        return nom, lieu, description

    def prompt_resultat(self):
        """Prompt pour déterminer les resultats"""
        resultat = input("Quel est le resultat? (J1 / J2 / N )")
        if resultat == "J1":
            return "J1"
        elif resultat == "J2":
            return "J2"
        elif resultat == "N":
            return "N"
