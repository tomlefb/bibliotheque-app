import re
from datetime import datetime


def valider_email(email: str) -> bool:
    """Vérifie que l'email a un format valide"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return bool(re.match(pattern, email))


def valider_non_vide(valeur: str, nom_champ: str) -> str:
    """Vérifie qu'un champ n'est pas vide, retourne la valeur nettoyée"""
    valeur = valeur.strip()
    if not valeur:
        raise ValueError(f"Le champ '{nom_champ}' est obligatoire")
    return valeur


def valider_entier_positif(valeur: str, nom_champ: str) -> int:
    """Convertit et valide un entier positif"""
    try:
        nombre = int(valeur)
        if nombre <= 0:
            raise ValueError(f"'{nom_champ}' doit être positif")
        return nombre
    except ValueError:
        raise ValueError(f"'{nom_champ}' doit être un nombre entier")


def valider_annee(valeur: str) -> int:
    """Valide une année (entre 1000 et année courante)"""
    annee = valider_entier_positif(valeur, "année")
    annee_courante = datetime.now().year

    if annee < 1000 or annee > annee_courante:
        raise ValueError(f"L'année doit être entre 1000 et {annee_courante}")
    return annee


def valider_choix_menu(choix: str, min_val: int, max_val: int) -> int:
    """Valide un choix de menu entre min et max"""
    try:
        choix_int = int(choix)
        if choix_int < min_val or choix_int > max_val:
            raise ValueError(f"Choix invalide. Entrez un nombre entre {min_val} et {max_val}")
        return choix_int
    except ValueError:
        raise ValueError(f"Choix invalide. Entrez un nombre entre {min_val} et {max_val}")
