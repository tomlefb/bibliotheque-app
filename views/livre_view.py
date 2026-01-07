from typing import Optional
from models import livre
from utils.formatters import (
    afficher_menu, afficher_tableau, confirmer, pause,
    afficher_message_succes, afficher_message_erreur
)
from utils.validators import valider_choix_menu, valider_non_vide, valider_annee
from config.settings import TITRE_MENU_LIVRES


def afficher_menu_livres() -> Optional[int]:
    """Affiche le menu de gestion des livres"""
    options = [
        "Lister tous les livres",
        "Rechercher un livre",
        "Voir détails d'un livre",
        "Ajouter un livre",
        "Modifier un livre",
        "Supprimer un livre",
        "Retour au menu principal"
    ]

    afficher_menu(TITRE_MENU_LIVRES, options)

    try:
        choix = input("\nChoix: ").strip()
        return valider_choix_menu(choix, 1, 7)
    except ValueError as e:
        print(f"\n✗ {e}")
        return None


def lister_livres():
    """Affiche la liste de tous les livres"""
    livres = livre.get_all()

    if not livres:
        afficher_message_erreur("Aucun livre trouvé")
        return

    headers = ["ID", "Titre", "Auteur", "Année"]
    lignes = [[l['id'], l['titre'], l['auteur'], l['annee_publication'] or 'N/A'] for l in livres]

    afficher_tableau(headers, lignes)
    pause()


def rechercher_livre():
    """Recherche des livres par titre ou auteur"""
    terme = input("\nRechercher (titre/auteur): ").strip()

    if not terme:
        afficher_message_erreur("Terme de recherche vide")
        return

    resultats = livre.search(terme)

    if not resultats:
        afficher_message_erreur(f"Aucun livre trouvé pour '{terme}'")
        return

    headers = ["ID", "Titre", "Auteur", "Année"]
    lignes = [[l['id'], l['titre'], l['auteur'], l['annee_publication'] or 'N/A'] for l in resultats]

    afficher_tableau(headers, lignes)
    pause()


def voir_details_livre():
    """Affiche les détails complets d'un livre"""
    try:
        livre_id = int(input("\nID du livre: ").strip())
        liv = livre.get_by_id(livre_id)

        if not liv:
            afficher_message_erreur(f"Livre avec l'ID {livre_id} non trouvé")
            return

        disponible = livre.est_disponible(livre_id)
        statut = "Disponible" if disponible else "Emprunté"

        print(f"\n{'='*50}")
        print(f"ID: {liv['id']}")
        print(f"Titre: {liv['titre']}")
        print(f"Auteur: {liv['auteur']}")
        print(f"Année: {liv['annee_publication'] or 'N/A'}")
        print(f"Statut: {statut}")
        print(f"{'='*50}\n")

        pause()
    except ValueError:
        afficher_message_erreur("ID invalide")


def ajouter_livre():
    """Ajoute un nouveau livre"""
    try:
        print("\n--- Ajouter un livre ---\n")
        titre = valider_non_vide(input("Titre: "), "titre")
        auteur = valider_non_vide(input("Auteur: "), "auteur")
        annee_input = input("Année de publication (optionnel): ").strip()

        annee = None
        if annee_input:
            annee = valider_annee(annee_input)

        livre_id = livre.create(titre, auteur, annee)

        if livre_id:
            afficher_message_succes(f"Livre créé avec l'ID: {livre_id}")
        else:
            afficher_message_erreur("Erreur lors de la création")

    except ValueError as e:
        afficher_message_erreur(str(e))
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def modifier_livre():
    """Modifie les informations d'un livre existant"""
    try:
        livre_id = int(input("\nID du livre à modifier: ").strip())
        liv = livre.get_by_id(livre_id)

        if not liv:
            afficher_message_erreur(f"Livre avec l'ID {livre_id} non trouvé")
            return

        print(f"\nLivre actuel: {liv['titre']} - {liv['auteur']} ({liv['annee_publication'] or 'N/A'})")
        print("\nNouvelles informations (Entrée pour garder l'actuel):\n")

        titre = input(f"Titre [{liv['titre']}]: ").strip() or liv['titre']
        auteur = input(f"Auteur [{liv['auteur']}]: ").strip() or liv['auteur']
        annee_input = input(f"Année [{liv['annee_publication'] or 'N/A'}]: ").strip()

        annee = liv['annee_publication']
        if annee_input and annee_input != 'N/A':
            annee = valider_annee(annee_input)

        if confirmer("Confirmer la modification?"):
            if livre.update(livre_id, titre, auteur, annee):
                afficher_message_succes("Livre modifié avec succès")
            else:
                afficher_message_erreur("Erreur lors de la modification")
        else:
            print("\nModification annulée")

    except ValueError as e:
        afficher_message_erreur(str(e))
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def supprimer_livre():
    """Supprime un livre après confirmation"""
    try:
        livre_id = int(input("\nID du livre à supprimer: ").strip())
        liv = livre.get_by_id(livre_id)

        if not liv:
            afficher_message_erreur(f"Livre avec l'ID {livre_id} non trouvé")
            return

        print(f"\nLivre: {liv['titre']} - {liv['auteur']}")

        if confirmer("ATTENTION: Confirmer la suppression?"):
            if livre.delete(livre_id):
                afficher_message_succes("Livre supprimé avec succès")
            else:
                afficher_message_erreur("Erreur lors de la suppression")
        else:
            print("\nSuppression annulée")

    except ValueError as e:
        afficher_message_erreur(str(e))
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()
