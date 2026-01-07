from typing import Optional, List, Dict
from datetime import date, timedelta
from config.database import execute_query
from config.settings import DUREE_EMPRUNT_DEFAUT, AMENDE_PAR_JOUR


def create(etudiant_id: int, isbn: str) -> Optional[int]:
    """Crée un emprunt et retourne son ID"""
    date_emprunt = date.today()

    query = """
        INSERT INTO emprunt (id_etud, isbn, date_emprunt, amende)
        VALUES (%s, %s, %s, 0)
        RETURNING id_emprunt
    """
    result = execute_query(query, (etudiant_id, isbn, date_emprunt), fetch_one=True)

    # Décrémenter exemplaires_dispo
    if result:
        execute_query("UPDATE livre SET exemplaires_dispo = exemplaires_dispo - 1 WHERE isbn = %s", (isbn,))

    return result['id_emprunt'] if result else None


def get_all() -> List[Dict]:
    """Retourne tous les emprunts avec détails étudiant et livre"""
    query = """
        SELECT e.id_emprunt as id, e.date_emprunt, e.date_retour, e.amende,
               et.id_etud as etudiant_id, et.nom, et.prenom,
               l.isbn as livre_id, l.titre, l.editeur as auteur
        FROM emprunt e
        JOIN etudiant et ON e.id_etud = et.id_etud
        JOIN livre l ON e.isbn = l.isbn
        ORDER BY e.date_emprunt DESC
    """
    return execute_query(query, fetch=True) or []


def get_by_id(emprunt_id: int) -> Optional[Dict]:
    """Retourne un emprunt par son ID avec détails"""
    query = """
        SELECT e.id_emprunt as id, e.date_emprunt, e.date_retour, e.amende,
               et.id_etud as etudiant_id, et.nom, et.prenom,
               l.isbn as livre_id, l.titre, l.editeur as auteur
        FROM emprunt e
        JOIN etudiant et ON e.id_etud = et.id_etud
        JOIN livre l ON e.isbn = l.isbn
        WHERE e.id_emprunt = %s
    """
    return execute_query(query, (emprunt_id,), fetch_one=True)


def get_by_etudiant(etudiant_id: int) -> List[Dict]:
    """Retourne tous les emprunts d'un étudiant"""
    query = """
        SELECT e.id_emprunt as id, e.date_emprunt, e.date_retour, e.amende,
               et.id_etud as etudiant_id, et.nom, et.prenom,
               l.isbn as livre_id, l.titre, l.editeur as auteur
        FROM emprunt e
        JOIN etudiant et ON e.id_etud = et.id_etud
        JOIN livre l ON e.isbn = l.isbn
        WHERE e.id_etud = %s
        ORDER BY e.date_emprunt DESC
    """
    return execute_query(query, (etudiant_id,), fetch=True) or []


def get_en_cours() -> List[Dict]:
    """Retourne tous les emprunts en cours (non retournés)"""
    query = """
        SELECT e.id_emprunt as id, e.date_emprunt, e.date_retour, e.amende,
               et.id_etud as etudiant_id, et.nom, et.prenom,
               l.isbn as livre_id, l.titre, l.editeur as auteur
        FROM emprunt e
        JOIN etudiant et ON e.id_etud = et.id_etud
        JOIN livre l ON e.isbn = l.isbn
        WHERE e.date_retour IS NULL
        ORDER BY e.date_emprunt
    """
    return execute_query(query, fetch=True) or []


def get_en_retard() -> List[Dict]:
    """Retourne tous les emprunts en retard"""
    date_limite = date.today() - timedelta(days=DUREE_EMPRUNT_DEFAUT)

    query = """
        SELECT e.id_emprunt as id, e.date_emprunt, e.date_retour, e.amende,
               et.id_etud as etudiant_id, et.nom, et.prenom,
               l.isbn as livre_id, l.titre, l.editeur as auteur
        FROM emprunt e
        JOIN etudiant et ON e.id_etud = et.id_etud
        JOIN livre l ON e.isbn = l.isbn
        WHERE e.date_retour IS NULL
        AND e.date_emprunt < %s
        ORDER BY e.date_emprunt
    """
    return execute_query(query, (date_limite,), fetch=True) or []


def retourner(emprunt_id: int) -> bool:
    """Marque un emprunt comme retourné avec la date du jour"""
    # Récupérer l'emprunt pour calculer l'amende
    emp = get_by_id(emprunt_id)
    if not emp:
        return False

    jours_retard = calculer_jours_retard(emp)
    amende_calc = jours_retard * AMENDE_PAR_JOUR

    # Mettre à jour l'emprunt
    query = """
        UPDATE emprunt
        SET date_retour = %s, amende = %s
        WHERE id_emprunt = %s AND date_retour IS NULL
    """
    result = execute_query(query, (date.today(), amende_calc, emprunt_id))

    # Incrémenter exemplaires_dispo
    if result and emp:
        execute_query("UPDATE livre SET exemplaires_dispo = exemplaires_dispo + 1 WHERE isbn = %s", (emp['livre_id'],))
        # Ajouter l'amende au solde de l'étudiant
        if amende_calc > 0:
            execute_query("UPDATE etudiant SET solde_amende = solde_amende + %s WHERE id_etud = %s", (amende_calc, emp['etudiant_id']))

    return result


def delete(emprunt_id: int) -> bool:
    """Supprime un emprunt"""
    return execute_query("DELETE FROM emprunt WHERE id_emprunt = %s", (emprunt_id,))


def calculer_jours_retard(emprunt: Dict) -> int:
    """Calcule le nombre de jours de retard pour un emprunt"""
    if emprunt['date_retour'] is not None:
        return 0

    date_emprunt = emprunt['date_emprunt']
    jours_ecoules = (date.today() - date_emprunt).days

    return max(0, jours_ecoules - DUREE_EMPRUNT_DEFAUT)


def calculer_amende(emprunt: Dict) -> float:
    """Calcule l'amende pour un emprunt en retard"""
    jours_retard = calculer_jours_retard(emprunt)
    return jours_retard * AMENDE_PAR_JOUR
