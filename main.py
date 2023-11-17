"""Point d'entré"""

from controllers import Controller
from views import View


def main():
    controller = Controller(
        view=View(),
    )
    controller.menu_principal()

if __name__ == "__main__":
    main()
