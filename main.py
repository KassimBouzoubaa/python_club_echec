"""Point d'entré"""

from controllers import Controller
from views import View
from models import Tournoi


def main():
    view = View()
    tournoi = Tournoi()

    game = Controller(view, tournoi)
    game.execution()


if __name__ == "__main__":
    main()
