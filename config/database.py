import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from utils.logger import log

load_dotenv()

# Configuration BDD depuis variables d'environnement
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "database": os.getenv("DB_NAME", "bibliotheque"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "admin123")
}


def get_connection():
    """Retourne une connexion à la base PostgreSQL"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        log(f"Erreur connexion BDD: {e}", level="ERROR")
        raise


def execute_query(query: str, params: tuple = None, fetch: bool = False, fetch_one: bool = False):
    """
    Exécute une requête SQL de manière sécurisée.

    Args:
        query: Requête SQL avec placeholders %s
        params: Paramètres de la requête
        fetch: True pour récupérer tous les résultats
        fetch_one: True pour récupérer un seul résultat

    Returns:
        Liste de dict, un dict, ou True si succès
    """
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params)

                if fetch_one:
                    return cur.fetchone()
                elif fetch:
                    return cur.fetchall()
                else:
                    conn.commit()
                    return True

    except psycopg2.Error as e:
        log(f"Erreur SQL: {e}", level="ERROR")
        raise


def test_connection() -> bool:
    """Teste la connexion à la base de données"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                return True
    except Exception as e:
        log(f"Test connexion échoué: {e}", level="ERROR")
        return False
