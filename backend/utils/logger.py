from datetime import datetime

LOG_FILE = "app.log"


def log(message: str, level: str = "INFO"):
    """
    Log un message dans le fichier et la console si erreur.
    Niveaux: INFO, ERROR, DEBUG
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = f"[{timestamp}] [{level}] {message}"

    # Toujours écrire dans le fichier
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(ligne + "\n")

    # Afficher en console seulement les erreurs
    if level == "ERROR":
        print(f"ERREUR: {message}")
