#!/usr/bin/env python3
"""
Application de gestion de bibliothèque universitaire
Point d'entrée principal
"""

import sys
from config.database import test_connection
from utils.logger import log
from utils.formatters import afficher_message_erreur
from views import menu
from views import etudiant_view
from views import livre_view
from views import emprunt_view
from views import stats_view


def gerer_menu_etudiants():
    """Gère le sous-menu des étudiants"""
    while True:
        choix = etudiant_view.afficher_menu_etudiants()

        if choix is None:
            continue

        if choix == 1:
            etudiant_view.lister_etudiants()
        elif choix == 2:
            etudiant_view.rechercher_etudiant()
        elif choix == 3:
            etudiant_view.voir_details_etudiant()
        elif choix == 4:
            etudiant_view.ajouter_etudiant()
        elif choix == 5:
            etudiant_view.modifier_etudiant()
        elif choix == 6:
            etudiant_view.supprimer_etudiant()
        elif choix == 7:
            break


def gerer_menu_livres():
    """Gère le sous-menu des livres"""
    while True:
        choix = livre_view.afficher_menu_livres()

        if choix is None:
            continue

        if choix == 1:
            livre_view.lister_livres()
        elif choix == 2:
            livre_view.rechercher_livre()
        elif choix == 3:
            livre_view.voir_details_livre()
        elif choix == 4:
            livre_view.ajouter_livre()
        elif choix == 5:
            livre_view.modifier_livre()
        elif choix == 6:
            livre_view.supprimer_livre()
        elif choix == 7:
            break


def gerer_menu_emprunts():
    """Gère le sous-menu des emprunts"""
    while True:
        choix = emprunt_view.afficher_menu_emprunts()

        if choix is None:
            continue

        if choix == 1:
            emprunt_view.lister_emprunts()
        elif choix == 2:
            emprunt_view.lister_emprunts_en_cours()
        elif choix == 3:
            emprunt_view.lister_emprunts_en_retard()
        elif choix == 4:
            emprunt_view.voir_emprunts_etudiant()
        elif choix == 5:
            emprunt_view.creer_emprunt()
        elif choix == 6:
            emprunt_view.retourner_livre()
        elif choix == 7:
            emprunt_view.supprimer_emprunt()
        elif choix == 8:
            break


def gerer_menu_stats():
    """Gère le sous-menu des statistiques"""
    while True:
        choix = stats_view.afficher_menu_stats()

        if choix is None:
            continue

        if choix == 1:
            stats_view.afficher_vue_ensemble()
        elif choix == 2:
            stats_view.afficher_top_etudiants()
        elif choix == 3:
            stats_view.afficher_top_livres()
        elif choix == 4:
            stats_view.afficher_emprunts_retard()
        elif choix == 5:
            break


def main():
    """Point d'entrée principal de l'application"""
    log("Démarrage de l'application")

    # Test de connexion à la base de données
    print("\nTest de connexion à la base de données...")
    if not test_connection():
        afficher_message_erreur("Impossible de se connecter à la base de données")
        afficher_message_erreur("Vérifiez votre fichier .env et que PostgreSQL est démarré")
        sys.exit(1)

    print("✓ Connexion réussie\n")

    # Boucle principale
    while True:
        try:
            choix = menu.afficher_menu_principal()

            if choix is None:
                continue

            if choix == 1:
                gerer_menu_etudiants()
            elif choix == 2:
                gerer_menu_livres()
            elif choix == 3:
                gerer_menu_emprunts()
            elif choix == 4:
                gerer_menu_stats()
            elif choix == 5:
                print("\nAu revoir!\n")
                log("Arrêt de l'application")
                break

        except KeyboardInterrupt:
            print("\n\nInterruption utilisateur")
            log("Arrêt de l'application (Ctrl+C)")
            break
        except Exception as e:
            afficher_message_erreur(f"Erreur inattendue: {e}")
            log(f"Erreur inattendue: {e}", level="ERROR")


if __name__ == "__main__":
    main()
