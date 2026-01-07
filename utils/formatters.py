from typing import List
from datetime import date
from config.settings import FORMAT_DATE


def afficher_tableau(headers: List[str], lignes: List[List], largeurs: List[int] = None):
    """Affiche un tableau formaté en console"""
    if not lignes:
        print("\nAucune donnée à afficher.\n")
        return

    if not largeurs:
        largeurs = []
        for i, h in enumerate(headers):
            max_data = max((len(str(row[i])) for row in lignes), default=0) if lignes else 0
            largeurs.append(max(len(h), max_data) + 2)

    sep = "+" + "+".join("-" * l for l in largeurs) + "+"

    print(sep)
    print("|" + "|".join(h.center(l) for h, l in zip(headers, largeurs)) + "|")
    print(sep)

    for ligne in lignes:
        print("|" + "|".join(str(c).ljust(l) for c, l in zip(ligne, largeurs)) + "|")

    print(sep)
    print(f"Total: {len(lignes)} ligne(s)\n")


def afficher_menu(titre: str, options: List[str]):
    """Affiche un menu avec titre et options numérotées"""
    largeur = max(len(titre), max(len(o) for o in options) + 4) + 4

    print("\n" + "=" * largeur)
    print(titre.center(largeur))
    print("=" * largeur)
    for i, opt in enumerate(options, 1):
        print(f"  {i}. {opt}")
    print("=" * largeur)


def confirmer(message: str) -> bool:
    """Demande une confirmation oui/non"""
    reponse = input(f"{message} (o/n): ").strip().lower()
    return reponse in ('o', 'oui', 'y', 'yes')


def pause():
    """Attend que l'utilisateur appuie sur Entrée"""
    input("\nAppuyez sur Entrée pour continuer...")


def formater_date(date_obj: date) -> str:
    """Formate une date selon le format défini"""
    if date_obj is None:
        return "N/A"
    return date_obj.strftime(FORMAT_DATE)


def afficher_message_succes(message: str):
    """Affiche un message de succès"""
    print(f"\n✓ {message}\n")


def afficher_message_erreur(message: str):
    """Affiche un message d'erreur"""
    print(f"\n✗ {message}\n")


def afficher_separateur():
    """Affiche une ligne de séparation"""
    print("\n" + "-" * 60 + "\n")
