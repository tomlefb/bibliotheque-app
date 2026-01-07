from typing import Optional
from models import etudiant
from utils.formatters import (
    afficher_menu, afficher_tableau, confirmer, pause,
    afficher_message_succes, afficher_message_erreur
)
from utils.validators import valider_choix_menu, valider_non_vide, valider_email
from config.settings import TITRE_MENU_ETUDIANTS


def afficher_menu_etudiants() -> Optional[int]:
    """Affiche le menu de gestion des étudiants"""
    options = [
        "Lister tous les étudiants",
        "Rechercher un étudiant",
        "Voir détails d'un étudiant",
        "Ajouter un étudiant",
        "Modifier un étudiant",
        "Supprimer un étudiant",
        "Retour au menu principal"
    ]

    afficher_menu(TITRE_MENU_ETUDIANTS, options)

    try:
        choix = input("\nChoix: ").strip()
        return valider_choix_menu(choix, 1, 7)
    except ValueError as e:
        print(f"\n✗ {e}")
        return None


def lister_etudiants():
    """Affiche la liste de tous les étudiants"""
    etudiants = etudiant.get_all()

    if not etudiants:
        afficher_message_erreur("Aucun étudiant trouvé")
        return

    headers = ["ID", "Nom", "Prénom", "Email"]
    lignes = [[e['id'], e['nom'], e['prenom'], e['email']] for e in etudiants]

    afficher_tableau(headers, lignes)
    pause()


def rechercher_etudiant():
    """Recherche des étudiants par nom, prénom ou email"""
    terme = input("\nRechercher (nom/prénom/email): ").strip()

    if not terme:
        afficher_message_erreur("Terme de recherche vide")
        return

    resultats = etudiant.search(terme)

    if not resultats:
        afficher_message_erreur(f"Aucun étudiant trouvé pour '{terme}'")
        return

    headers = ["ID", "Nom", "Prénom", "Email"]
    lignes = [[e['id'], e['nom'], e['prenom'], e['email']] for e in resultats]

    afficher_tableau(headers, lignes)
    pause()


def voir_details_etudiant():
    """Affiche les détails complets d'un étudiant"""
    try:
        etudiant_id = int(input("\nID de l'étudiant: ").strip())
        etud = etudiant.get_by_id(etudiant_id)

        if not etud:
            afficher_message_erreur(f"Étudiant avec l'ID {etudiant_id} non trouvé")
            return

        print(f"\n{'='*50}")
        print(f"ID: {etud['id']}")
        print(f"Nom: {etud['nom']}")
        print(f"Prénom: {etud['prenom']}")
        print(f"Email: {etud['email']}")

        nb_emprunts = etudiant.count_emprunts_actifs(etudiant_id)
        print(f"Emprunts en cours: {nb_emprunts}")
        print(f"{'='*50}\n")

        pause()
    except ValueError:
        afficher_message_erreur("ID invalide")


def ajouter_etudiant():
    """Ajoute un nouvel étudiant"""
    try:
        print("\n--- Ajouter un étudiant ---\n")
        nom = valider_non_vide(input("Nom: "), "nom")
        prenom = valider_non_vide(input("Prénom: "), "prénom")
        email_input = valider_non_vide(input("Email: "), "email")

        if not valider_email(email_input):
            afficher_message_erreur("Format d'email invalide")
            return

        etudiant_id = etudiant.create(nom, prenom, email_input)

        if etudiant_id:
            afficher_message_succes(f"Étudiant créé avec l'ID: {etudiant_id}")
        else:
            afficher_message_erreur("Erreur lors de la création")

    except ValueError as e:
        afficher_message_erreur(str(e))
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def modifier_etudiant():
    """Modifie les informations d'un étudiant existant"""
    try:
        etudiant_id = int(input("\nID de l'étudiant à modifier: ").strip())
        etud = etudiant.get_by_id(etudiant_id)

        if not etud:
            afficher_message_erreur(f"Étudiant avec l'ID {etudiant_id} non trouvé")
            return

        print(f"\nÉtudiant actuel: {etud['nom']} {etud['prenom']} - {etud['email']}")
        print("\nNouvelles informations (Entrée pour garder l'actuel):\n")

        nom = input(f"Nom [{etud['nom']}]: ").strip() or etud['nom']
        prenom = input(f"Prénom [{etud['prenom']}]: ").strip() or etud['prenom']
        email_input = input(f"Email [{etud['email']}]: ").strip() or etud['email']

        if email_input != etud['email'] and not valider_email(email_input):
            afficher_message_erreur("Format d'email invalide")
            return

        if confirmer("Confirmer la modification?"):
            if etudiant.update(etudiant_id, nom, prenom, email_input):
                afficher_message_succes("Étudiant modifié avec succès")
            else:
                afficher_message_erreur("Erreur lors de la modification")
        else:
            print("\nModification annulée")

    except ValueError:
        afficher_message_erreur("ID invalide")
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def supprimer_etudiant():
    """Supprime un étudiant après confirmation"""
    try:
        etudiant_id = int(input("\nID de l'étudiant à supprimer: ").strip())
        etud = etudiant.get_by_id(etudiant_id)

        if not etud:
            afficher_message_erreur(f"Étudiant avec l'ID {etudiant_id} non trouvé")
            return

        print(f"\nÉtudiant: {etud['nom']} {etud['prenom']} - {etud['email']}")

        if confirmer("ATTENTION: Confirmer la suppression?"):
            if etudiant.delete(etudiant_id):
                afficher_message_succes("Étudiant supprimé avec succès")
            else:
                afficher_message_erreur("Erreur lors de la suppression")
        else:
            print("\nSuppression annulée")

    except ValueError as e:
        afficher_message_erreur(str(e))
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()
