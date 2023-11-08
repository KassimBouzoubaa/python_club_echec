"""Point d'entré"""

from controllers import Controller
from views import View
from models import Tournoi


def main():
    controller = Controller(
        view=View(),
    )
    controller.menu_selection()

if __name__ == "__main__":
    main()
