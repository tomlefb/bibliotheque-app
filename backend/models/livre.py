from typing import Optional, List, Dict
from config.database import execute_query


def create(titre: str, editeur: str, isbn: str, annee: Optional[int] = None, exemplaires: int = 1) -> Optional[str]:
    """Crée un livre et retourne son ISBN"""
    query = """
        INSERT INTO livre (isbn, titre, editeur, annee, exemplaires_dispo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING isbn
    """
    result = execute_query(query, (isbn, titre, editeur, annee, exemplaires), fetch_one=True)
    return result['isbn'] if result else None


def get_all() -> List[Dict]:
    """Retourne tous les livres triés par titre"""
    query = "SELECT isbn, titre, editeur, annee as annee_publication, exemplaires_dispo FROM livre ORDER BY titre"
    return execute_query(query, fetch=True) or []


def get_by_id(isbn: str) -> Optional[Dict]:
    """Retourne un livre par son ISBN"""
    query = "SELECT isbn, titre, editeur, annee as annee_publication, exemplaires_dispo FROM livre WHERE isbn = %s"
    return execute_query(query, (isbn,), fetch_one=True)


def search(terme: str) -> List[Dict]:
    """Recherche un livre par titre ou editeur"""
    query = """
        SELECT isbn, titre, editeur, annee as annee_publication, exemplaires_dispo
        FROM livre
        WHERE titre ILIKE %s OR editeur ILIKE %s
        ORDER BY titre
    """
    pattern = f"%{terme}%"
    return execute_query(query, (pattern, pattern), fetch=True) or []


def update(isbn: str, titre: str, editeur: str, annee: Optional[int] = None) -> bool:
    """Met à jour les infos d'un livre"""
    query = """
        UPDATE livre
        SET titre = %s, editeur = %s, annee = %s
        WHERE isbn = %s
    """
    return execute_query(query, (titre, editeur, annee, isbn))


def delete(isbn: str) -> bool:
    """
    Supprime un livre.
    Lève une erreur si des emprunts sont liés.
    """
    # Vérifier les emprunts liés
    check = execute_query(
        "SELECT COUNT(*) as count FROM emprunt WHERE isbn = %s",
        (isbn,),
        fetch_one=True
    )

    if check and check['count'] > 0:
        raise ValueError(f"Impossible: {check['count']} emprunt(s) lié(s)")

    return execute_query("DELETE FROM livre WHERE isbn = %s", (isbn,))


def exists(isbn: str) -> bool:
    """Vérifie si un livre existe"""
    result = execute_query(
        "SELECT 1 FROM livre WHERE isbn = %s",
        (isbn,),
        fetch_one=True
    )
    return result is not None


def est_disponible(isbn: str) -> bool:
    """Vérifie si un livre est actuellement disponible"""
    result = execute_query(
        "SELECT exemplaires_dispo FROM livre WHERE isbn = %s",
        (isbn,),
        fetch_one=True
    )
    return result is not None and result['exemplaires_dispo'] > 0
