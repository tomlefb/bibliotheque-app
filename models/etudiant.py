from typing import Optional, List, Dict
from config.database import execute_query


def create(nom: str, prenom: str, email: str) -> Optional[int]:
    """Crée un étudiant et retourne son ID"""
    query = """
        INSERT INTO etudiant (nom, prenom, email, date_inscription, solde_amende)
        VALUES (%s, %s, %s, CURRENT_DATE, 0)
        RETURNING id_etud
    """
    result = execute_query(query, (nom, prenom, email), fetch_one=True)
    return result['id_etud'] if result else None


def get_all() -> List[Dict]:
    """Retourne tous les étudiants triés par nom"""
    query = "SELECT id_etud as id, nom, prenom, email, date_inscription, solde_amende FROM etudiant ORDER BY nom, prenom"
    return execute_query(query, fetch=True) or []


def get_by_id(etudiant_id: int) -> Optional[Dict]:
    """Retourne un étudiant par son ID"""
    query = "SELECT id_etud as id, nom, prenom, email, date_inscription, solde_amende FROM etudiant WHERE id_etud = %s"
    return execute_query(query, (etudiant_id,), fetch_one=True)


def search(terme: str) -> List[Dict]:
    """Recherche un étudiant par nom, prénom ou email"""
    query = """
        SELECT id_etud as id, nom, prenom, email, date_inscription, solde_amende
        FROM etudiant
        WHERE nom ILIKE %s OR prenom ILIKE %s OR email ILIKE %s
        ORDER BY nom, prenom
    """
    pattern = f"%{terme}%"
    return execute_query(query, (pattern, pattern, pattern), fetch=True) or []


def update(etudiant_id: int, nom: str, prenom: str, email: str) -> bool:
    """Met à jour les infos d'un étudiant"""
    query = """
        UPDATE etudiant
        SET nom = %s, prenom = %s, email = %s
        WHERE id_etud = %s
    """
    return execute_query(query, (nom, prenom, email, etudiant_id))


def delete(etudiant_id: int) -> bool:
    """
    Supprime un étudiant.
    Lève une erreur si des emprunts sont liés.
    """
    # Vérifier les emprunts liés
    check = execute_query(
        "SELECT COUNT(*) as count FROM emprunt WHERE id_etud = %s",
        (etudiant_id,),
        fetch_one=True
    )

    if check and check['count'] > 0:
        raise ValueError(f"Impossible: {check['count']} emprunt(s) lié(s)")

    return execute_query("DELETE FROM etudiant WHERE id_etud = %s", (etudiant_id,))


def exists(etudiant_id: int) -> bool:
    """Vérifie si un étudiant existe"""
    result = execute_query(
        "SELECT 1 FROM etudiant WHERE id_etud = %s",
        (etudiant_id,),
        fetch_one=True
    )
    return result is not None


def count_emprunts_actifs(etudiant_id: int) -> int:
    """Compte le nombre d'emprunts en cours pour un étudiant"""
    result = execute_query(
        "SELECT COUNT(*) as count FROM emprunt WHERE id_etud = %s AND date_retour IS NULL",
        (etudiant_id,),
        fetch_one=True
    )
    return result['count'] if result else 0
