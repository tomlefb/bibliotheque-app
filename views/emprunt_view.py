from typing import Optional
from models import emprunt, etudiant, livre
from utils.formatters import (
    afficher_menu, afficher_tableau, confirmer, pause,
    afficher_message_succes, afficher_message_erreur, formater_date
)
from utils.validators import valider_choix_menu
from config.settings import TITRE_MENU_EMPRUNTS, MAX_EMPRUNTS_PAR_ETUDIANT


def afficher_menu_emprunts() -> Optional[int]:
    """Affiche le menu de gestion des emprunts"""
    options = [
        "Lister tous les emprunts",
        "Lister emprunts en cours",
        "Lister emprunts en retard",
        "Voir emprunts d'un étudiant",
        "Créer un emprunt",
        "Retourner un livre",
        "Supprimer un emprunt",
        "Retour au menu principal"
    ]

    afficher_menu(TITRE_MENU_EMPRUNTS, options)

    try:
        choix = input("\nChoix: ").strip()
        return valider_choix_menu(choix, 1, 8)
    except ValueError as e:
        print(f"\n✗ {e}")
        return None


def lister_emprunts():
    """Affiche la liste de tous les emprunts"""
    emprunts = emprunt.get_all()

    if not emprunts:
        afficher_message_erreur("Aucun emprunt trouvé")
        return

    headers = ["ID", "Étudiant", "Livre", "Date emprunt", "Date retour"]
    lignes = [
        [
            e['id'],
            f"{e['nom']} {e['prenom']}",
            e['titre'],
            formater_date(e['date_emprunt']),
            formater_date(e['date_retour'])
        ]
        for e in emprunts
    ]

    afficher_tableau(headers, lignes)
    pause()


def lister_emprunts_en_cours():
    """Affiche la liste des emprunts en cours"""
    emprunts = emprunt.get_en_cours()

    if not emprunts:
        afficher_message_erreur("Aucun emprunt en cours")
        return

    headers = ["ID", "Étudiant", "Livre", "Date emprunt", "Jours", "Amende"]
    lignes = []

    for e in emprunts:
        jours_retard = emprunt.calculer_jours_retard(e)
        amende = emprunt.calculer_amende(e)
        lignes.append([
            e['id'],
            f"{e['nom']} {e['prenom']}",
            e['titre'],
            formater_date(e['date_emprunt']),
            jours_retard if jours_retard > 0 else "-",
            f"{amende:.2f}€" if amende > 0 else "-"
        ])

    afficher_tableau(headers, lignes)
    pause()


def lister_emprunts_en_retard():
    """Affiche la liste des emprunts en retard avec amendes"""
    emprunts = emprunt.get_en_retard()

    if not emprunts:
        afficher_message_succes("Aucun emprunt en retard!")
        pause()
        return

    headers = ["ID", "Étudiant", "Livre", "Date emprunt", "Jours retard", "Amende"]
    lignes = []

    for e in emprunts:
        jours_retard = emprunt.calculer_jours_retard(e)
        amende = emprunt.calculer_amende(e)
        lignes.append([
            e['id'],
            f"{e['nom']} {e['prenom']}",
            e['titre'],
            formater_date(e['date_emprunt']),
            jours_retard,
            f"{amende:.2f}€"
        ])

    afficher_tableau(headers, lignes)
    pause()


def voir_emprunts_etudiant():
    """Affiche tous les emprunts d'un étudiant"""
    try:
        etudiant_id = int(input("\nID de l'étudiant: ").strip())

        if not etudiant.exists(etudiant_id):
            afficher_message_erreur(f"Étudiant avec l'ID {etudiant_id} non trouvé")
            return

        emprunts = emprunt.get_by_etudiant(etudiant_id)

        if not emprunts:
            afficher_message_erreur("Aucun emprunt pour cet étudiant")
            return

        headers = ["ID", "Livre", "Date emprunt", "Date retour"]
        lignes = [
            [
                e['id'],
                e['titre'],
                formater_date(e['date_emprunt']),
                formater_date(e['date_retour'])
            ]
            for e in emprunts
        ]

        afficher_tableau(headers, lignes)
        pause()

    except ValueError:
        afficher_message_erreur("ID invalide")


def creer_emprunt():
    """Crée un nouveau emprunt"""
    try:
        print("\n--- Créer un emprunt ---\n")
        etudiant_id = int(input("ID de l'étudiant: ").strip())
        livre_id = int(input("ID du livre: ").strip())

        # Vérifications
        if not etudiant.exists(etudiant_id):
            afficher_message_erreur(f"Étudiant avec l'ID {etudiant_id} non trouvé")
            return

        if not livre.exists(livre_id):
            afficher_message_erreur(f"Livre avec l'ID {livre_id} non trouvé")
            return

        if not livre.est_disponible(livre_id):
            afficher_message_erreur("Ce livre est déjà emprunté")
            return

        nb_emprunts = etudiant.count_emprunts_actifs(etudiant_id)
        if nb_emprunts >= MAX_EMPRUNTS_PAR_ETUDIANT:
            afficher_message_erreur(f"Limite atteinte: {MAX_EMPRUNTS_PAR_ETUDIANT} emprunts max par étudiant")
            return

        emprunt_id = emprunt.create(etudiant_id, livre_id)

        if emprunt_id:
            afficher_message_succes(f"Emprunt créé avec l'ID: {emprunt_id}")
        else:
            afficher_message_erreur("Erreur lors de la création")

    except ValueError:
        afficher_message_erreur("ID invalide")
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def retourner_livre():
    """Marque un emprunt comme retourné"""
    try:
        emprunt_id = int(input("\nID de l'emprunt à retourner: ").strip())
        emp = emprunt.get_by_id(emprunt_id)

        if not emp:
            afficher_message_erreur(f"Emprunt avec l'ID {emprunt_id} non trouvé")
            return

        if emp['date_retour'] is not None:
            afficher_message_erreur("Ce livre a déjà été retourné")
            return

        print(f"\nEmprunt: {emp['nom']} {emp['prenom']} - {emp['titre']}")
        print(f"Date d'emprunt: {formater_date(emp['date_emprunt'])}")

        jours_retard = emprunt.calculer_jours_retard(emp)
        amende = emprunt.calculer_amende(emp)

        if jours_retard > 0:
            print(f"\n⚠ RETARD: {jours_retard} jour(s)")
            print(f"Amende: {amende:.2f}€")

        if confirmer("Confirmer le retour?"):
            if emprunt.retourner(emprunt_id):
                afficher_message_succes("Livre retourné avec succès")
                if amende > 0:
                    print(f"Amende à collecter: {amende:.2f}€")
            else:
                afficher_message_erreur("Erreur lors du retour")
        else:
            print("\nRetour annulé")

    except ValueError:
        afficher_message_erreur("ID invalide")
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()


def supprimer_emprunt():
    """Supprime un emprunt après confirmation"""
    try:
        emprunt_id = int(input("\nID de l'emprunt à supprimer: ").strip())
        emp = emprunt.get_by_id(emprunt_id)

        if not emp:
            afficher_message_erreur(f"Emprunt avec l'ID {emprunt_id} non trouvé")
            return

        print(f"\nEmprunt: {emp['nom']} {emp['prenom']} - {emp['titre']}")

        if confirmer("ATTENTION: Confirmer la suppression?"):
            if emprunt.delete(emprunt_id):
                afficher_message_succes("Emprunt supprimé avec succès")
            else:
                afficher_message_erreur("Erreur lors de la suppression")
        else:
            print("\nSuppression annulée")

    except ValueError:
        afficher_message_erreur("ID invalide")
    except Exception as e:
        afficher_message_erreur(f"Erreur: {e}")

    pause()
