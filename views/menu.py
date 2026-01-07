from utils.formatters import afficher_menu
from utils.validators import valider_choix_menu
from config.settings import TITRE_APP


def afficher_menu_principal():
    """Affiche le menu principal et retourne le choix de l'utilisateur"""
    options = [
        "Gérer les étudiants",
        "Gérer les livres",
        "Gérer les emprunts",
        "Statistiques",
        "Quitter"
    ]

    afficher_menu(TITRE_APP, options)

    try:
        choix = input("\nChoix: ").strip()
        return valider_choix_menu(choix, 1, 5)
    except ValueError as e:
        print(f"\n✗ {e}")
        return None
