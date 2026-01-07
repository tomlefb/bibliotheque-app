from typing import Dict, List
from config.database import execute_query


def get_totaux() -> Dict:
    """Retourne le nombre total d'étudiants, livres et emprunts"""
    query_etudiants = "SELECT COUNT(*) as total FROM etudiant"
    query_livres = "SELECT COUNT(*) as total FROM livre"
    query_emprunts = "SELECT COUNT(*) as total FROM emprunt"

    total_etudiants = execute_query(query_etudiants, fetch_one=True)
    total_livres = execute_query(query_livres, fetch_one=True)
    total_emprunts = execute_query(query_emprunts, fetch_one=True)

    return {
        'etudiants': total_etudiants['total'] if total_etudiants else 0,
        'livres': total_livres['total'] if total_livres else 0,
        'emprunts': total_emprunts['total'] if total_emprunts else 0
    }


def get_top_etudiants(limit: int = 5) -> List[Dict]:
    """Retourne les étudiants ayant le plus d'emprunts"""
    query = """
        SELECT et.id_etud as id, et.nom, et.prenom, COUNT(e.id_emprunt) as nombre_emprunts
        FROM etudiant et
        LEFT JOIN emprunt e ON et.id_etud = e.id_etud
        GROUP BY et.id_etud, et.nom, et.prenom
        HAVING COUNT(e.id_emprunt) > 0
        ORDER BY nombre_emprunts DESC
        LIMIT %s
    """
    return execute_query(query, (limit,), fetch=True) or []


def get_top_livres(limit: int = 5) -> List[Dict]:
    """Retourne les livres les plus empruntés"""
    query = """
        SELECT l.isbn, l.titre, l.editeur as auteur, COUNT(e.id_emprunt) as nombre_emprunts
        FROM livre l
        LEFT JOIN emprunt e ON l.isbn = e.isbn
        GROUP BY l.isbn, l.titre, l.editeur
        HAVING COUNT(e.id_emprunt) > 0
        ORDER BY nombre_emprunts DESC
        LIMIT %s
    """
    return execute_query(query, (limit,), fetch=True) or []


def get_stats_emprunts() -> Dict:
    """Retourne des statistiques sur les emprunts"""
    query_en_cours = "SELECT COUNT(*) as total FROM emprunt WHERE date_retour IS NULL"
    query_termines = "SELECT COUNT(*) as total FROM emprunt WHERE date_retour IS NOT NULL"

    en_cours = execute_query(query_en_cours, fetch_one=True)
    termines = execute_query(query_termines, fetch_one=True)

    return {
        'en_cours': en_cours['total'] if en_cours else 0,
        'termines': termines['total'] if termines else 0
    }


def get_livres_disponibles() -> int:
    """Retourne le nombre total d'exemplaires disponibles"""
    query = "SELECT SUM(exemplaires_dispo) as total FROM livre"
    result = execute_query(query, fetch_one=True)
    return result['total'] if result and result['total'] else 0


def get_taux_emprunt() -> float:
    """Calcule le taux d'emprunts actifs par rapport au total d'exemplaires"""
    # Total exemplaires
    total_exemplaires = execute_query(
        "SELECT SUM(exemplaires_dispo) as total FROM livre",
        fetch_one=True
    )

    # Emprunts actifs
    emprunts_actifs = execute_query(
        "SELECT COUNT(*) as total FROM emprunt WHERE date_retour IS NULL",
        fetch_one=True
    )

    if not total_exemplaires or total_exemplaires['total'] == 0:
        return 0.0

    total = total_exemplaires['total']
    actifs = emprunts_actifs['total'] if emprunts_actifs else 0

    return (actifs / total) * 100 if total > 0 else 0.0
