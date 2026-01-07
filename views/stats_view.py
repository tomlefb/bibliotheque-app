from typing import Optional
from services import stats_service
from models import emprunt
from utils.formatters import (
    afficher_menu, afficher_tableau, pause, afficher_separateur
)
from utils.validators import valider_choix_menu
from config.settings import TITRE_MENU_STATS


def afficher_menu_stats() -> Optional[int]:
    """Affiche le menu des statistiques"""
    options = [
        "Vue d'ensemble",
        "Top 5 étudiants (plus d'emprunts)",
        "Top 5 livres (plus empruntés)",
        "Emprunts en retard avec amendes",
        "Retour au menu principal"
    ]

    afficher_menu(TITRE_MENU_STATS, options)

    try:
        choix = input("\nChoix: ").strip()
        return valider_choix_menu(choix, 1, 5)
    except ValueError as e:
        print(f"\n✗ {e}")
        return None


def afficher_vue_ensemble():
    """Affiche une vue d'ensemble des statistiques"""
    totaux = stats_service.get_totaux()
    stats_emprunts = stats_service.get_stats_emprunts()
    livres_dispo = stats_service.get_livres_disponibles()
    taux = stats_service.get_taux_emprunt()

    print("\n" + "="*60)
    print("VUE D'ENSEMBLE".center(60))
    print("="*60)

    print(f"\nÉtudiants inscrits: {totaux['etudiants']}")
    print(f"Livres au catalogue: {totaux['livres']}")
    print(f"Total emprunts (historique): {totaux['emprunts']}")

    afficher_separateur()

    print(f"Emprunts en cours: {stats_emprunts['en_cours']}")
    print(f"Emprunts terminés: {stats_emprunts['termines']}")
    print(f"Livres disponibles: {livres_dispo}")
    print(f"Taux d'emprunt: {taux:.1f}%")

    print("="*60 + "\n")

    pause()


def afficher_top_etudiants():
    """Affiche le top 5 des étudiants ayant le plus emprunté"""
    top = stats_service.get_top_etudiants(5)

    if not top:
        print("\nAucune donnée disponible\n")
        pause()
        return

    headers = ["#", "ID", "Nom", "Prénom", "Nb emprunts"]
    lignes = [
        [i+1, e['id'], e['nom'], e['prenom'], e['nb_emprunts']]
        for i, e in enumerate(top)
    ]

    print("\n" + "="*60)
    print("TOP 5 ÉTUDIANTS".center(60))
    print("="*60 + "\n")

    afficher_tableau(headers, lignes)
    pause()


def afficher_top_livres():
    """Affiche le top 5 des livres les plus empruntés"""
    top = stats_service.get_top_livres(5)

    if not top:
        print("\nAucune donnée disponible\n")
        pause()
        return

    headers = ["#", "ID", "Titre", "Auteur", "Nb emprunts"]
    lignes = [
        [i+1, l['id'], l['titre'], l['auteur'], l['nb_emprunts']]
        for i, l in enumerate(top)
    ]

    print("\n" + "="*60)
    print("TOP 5 LIVRES".center(60))
    print("="*60 + "\n")

    afficher_tableau(headers, lignes)
    pause()


def afficher_emprunts_retard():
    """Affiche les emprunts en retard avec calcul des amendes"""
    emprunts = emprunt.get_en_retard()

    if not emprunts:
        print("\n✓ Aucun emprunt en retard!\n")
        pause()
        return

    headers = ["ID", "Étudiant", "Livre", "Jours retard", "Amende"]
    lignes = []
    total_amendes = 0.0

    for e in emprunts:
        jours_retard = emprunt.calculer_jours_retard(e)
        amende = emprunt.calculer_amende(e)
        total_amendes += amende

        lignes.append([
            e['id'],
            f"{e['nom']} {e['prenom']}",
            e['titre'],
            jours_retard,
            f"{amende:.2f}€"
        ])

    print("\n" + "="*60)
    print("EMPRUNTS EN RETARD".center(60))
    print("="*60 + "\n")

    afficher_tableau(headers, lignes)

    print(f"Total amendes à collecter: {total_amendes:.2f}€\n")
    print("="*60 + "\n")

    pause()
