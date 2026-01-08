# Documentation Backend - Administration BDD

**Projet** : Application de Gestion de Bibliothèque
**Auteurs** : Tom LEFEVRE-BONZON & Ilies MAHOUDEAU
**Module** : Administration de Bases de Données - B3 Dev SDV

---

## 1. Vue d'ensemble

Le backend est une **API REST** développée en Python avec Flask. Il sert d'intermédiaire entre le frontend (Angular) et la base de données PostgreSQL.

```
┌─────────────┐      HTTP/JSON      ┌─────────────┐      SQL      ┌─────────────┐
│   Frontend  │ ◄──────────────────► │   Backend   │ ◄────────────► │ PostgreSQL  │
│   Angular   │                      │   Flask     │                │             │
└─────────────┘                      └─────────────┘                └─────────────┘
     :4200                               :5001                         :5432
```

---

## 2. Structure du projet

```
backend/
├── app.py                 # Point d'entrée - Routes de l'API
├── config/
│   ├── __init__.py
│   ├── database.py        # Connexion et requêtes PostgreSQL
│   └── settings.py        # Configuration générale
├── models/
│   ├── __init__.py
│   ├── etudiant.py        # CRUD Étudiants
│   ├── livre.py           # CRUD Livres
│   └── emprunt.py         # CRUD Emprunts + calculs
├── services/
│   ├── __init__.py
│   └── stats_service.py   # Statistiques et agrégations
├── utils/
│   ├── __init__.py
│   ├── validators.py      # Validation des données
│   ├── formatters.py      # Formatage des résultats
│   └── logger.py          # Journalisation
├── sql/
│   ├── init.sql           # Création des tables
│   └── seed.sql           # Données de test
├── .env                   # Variables d'environnement (non versionné)
└── requirements.txt       # Dépendances Python
```

---

## 3. Base de données PostgreSQL

### 3.1 Modèle Conceptuel de Données (MCD)

On a 3 entités principales avec une relation N:N entre Étudiant et Livre via la table Emprunt :

```
ETUDIANT (1,n) ───── emprunte ───── (0,n) LIVRE
                         │
                         ▼
                     EMPRUNT
```

**Cardinalités** :
- Un étudiant peut emprunter plusieurs livres (1,n)
- Un livre peut être emprunté par plusieurs étudiants (0,n)
- La table EMPRUNT matérialise cette relation many-to-many

### 3.2 Modèle Logique de Données (MLD)

```
ETUDIANT (id, nom, prenom, email, created_at)
    - id : clé primaire (SERIAL)
    - email : contrainte UNIQUE

LIVRE (isbn, titre, editeur, annee_publication, exemplaires_dispo, created_at)
    - isbn : clé primaire (VARCHAR)
    - annee_publication : contrainte CHECK

EMPRUNT (id, etudiant_id, livre_isbn, date_emprunt, date_retour, created_at)
    - id : clé primaire (SERIAL)
    - etudiant_id : clé étrangère → ETUDIANT(id)
    - livre_isbn : clé étrangère → LIVRE(isbn)
    - date_retour : NULL si pas encore retourné
```

### 3.3 Script de création (init.sql)

```sql
-- Suppression des tables existantes (ordre important à cause des FK)
DROP TABLE IF EXISTS emprunt CASCADE;
DROP TABLE IF EXISTS livre CASCADE;
DROP TABLE IF EXISTS etudiant CASCADE;

-- Table ETUDIANT
CREATE TABLE etudiant (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table LIVRE
CREATE TABLE livre (
    isbn VARCHAR(20) PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    editeur VARCHAR(200) NOT NULL,
    annee_publication INTEGER,
    exemplaires_dispo INTEGER DEFAULT 1 CHECK (exemplaires_dispo >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (annee_publication IS NULL OR
           annee_publication BETWEEN 1000 AND EXTRACT(YEAR FROM CURRENT_DATE) + 1)
);

-- Table EMPRUNT (table de liaison)
CREATE TABLE emprunt (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL,
    livre_isbn VARCHAR(20) NOT NULL,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Clés étrangères
    CONSTRAINT fk_etudiant FOREIGN KEY (etudiant_id)
        REFERENCES etudiant(id) ON DELETE RESTRICT,
    CONSTRAINT fk_livre FOREIGN KEY (livre_isbn)
        REFERENCES livre(isbn) ON DELETE RESTRICT,

    -- Contrainte : date_retour >= date_emprunt
    CONSTRAINT chk_dates CHECK (date_retour IS NULL OR date_retour >= date_emprunt)
);
```

### 3.4 Contraintes d'intégrité

| Type | Table | Colonne | Description |
|------|-------|---------|-------------|
| **PRIMARY KEY** | etudiant | id | Identifiant auto-incrémenté |
| **PRIMARY KEY** | livre | isbn | ISBN unique du livre |
| **PRIMARY KEY** | emprunt | id | Identifiant auto-incrémenté |
| **FOREIGN KEY** | emprunt | etudiant_id | Référence vers etudiant.id |
| **FOREIGN KEY** | emprunt | livre_isbn | Référence vers livre.isbn |
| **UNIQUE** | etudiant | email | Pas de doublons d'email |
| **NOT NULL** | toutes | plusieurs | Champs obligatoires |
| **CHECK** | livre | annee_publication | Année entre 1000 et année courante |
| **CHECK** | livre | exemplaires_dispo | Doit être >= 0 |
| **CHECK** | emprunt | dates | date_retour >= date_emprunt |
| **DEFAULT** | plusieurs | created_at | Timestamp automatique |
| **ON DELETE RESTRICT** | emprunt | FK | Empêche suppression si emprunts liés |

**Pourquoi ON DELETE RESTRICT ?**
- Si on supprime un étudiant qui a des emprunts en cours, la BDD refuse
- Ça évite d'avoir des emprunts orphelins (sans étudiant associé)
- C'est une protection au niveau BDD, pas juste au niveau application

### 3.5 Index pour optimisation

```sql
-- Index sur les colonnes fréquemment recherchées
CREATE INDEX idx_etudiant_nom ON etudiant(nom);
CREATE INDEX idx_etudiant_email ON etudiant(email);
CREATE INDEX idx_livre_titre ON livre(titre);

-- Index sur les clés étrangères (améliore les JOIN)
CREATE INDEX idx_emprunt_etudiant ON emprunt(etudiant_id);
CREATE INDEX idx_emprunt_livre ON emprunt(livre_isbn);

-- Index sur date_retour (pour filtrer les emprunts en cours)
CREATE INDEX idx_emprunt_date_retour ON emprunt(date_retour);
```

**Pourquoi ces index ?**
- `idx_etudiant_nom` : recherche d'étudiants par nom
- `idx_emprunt_date_retour` : filtre `WHERE date_retour IS NULL` (emprunts en cours)
- Index sur FK : accélère les jointures entre tables

---

## 4. Connexion Python/PostgreSQL

### 4.1 Configuration (config/database.py)

```python
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables depuis .env

# Configuration depuis variables d'environnement
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),        # localhost
    "port": int(os.getenv("DB_PORT")),   # 5432
    "database": os.getenv("DB_NAME"),    # bibliotheque
    "user": os.getenv("DB_USER"),        # postgres
    "password": os.getenv("DB_PASSWORD") # ****
}

def get_connection():
    """Retourne une connexion à PostgreSQL"""
    return psycopg2.connect(**DB_CONFIG)
```

**Pourquoi des variables d'environnement ?**
- Le mot de passe n'est pas dans le code (sécurité)
- On peut changer la config sans modifier le code
- Fichier `.env` non versionné sur Git

### 4.2 Exécution sécurisée des requêtes

```python
def execute_query(query: str, params: tuple = None, fetch: bool = False, fetch_one: bool = False):
    """
    Exécute une requête SQL de manière sécurisée.

    Args:
        query: Requête SQL avec placeholders %s
        params: Tuple de paramètres
        fetch: True pour SELECT (plusieurs résultats)
        fetch_one: True pour SELECT (un seul résultat)

    Returns:
        - Liste de dict si fetch=True
        - Dict si fetch_one=True
        - True si INSERT/UPDATE/DELETE
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
```

**Points importants :**

1. **Context manager (`with`)** : ferme automatiquement la connexion
2. **RealDictCursor** : retourne des dictionnaires au lieu de tuples
3. **Requêtes paramétrées** : protection contre les injections SQL

### 4.3 Protection contre les injections SQL

```python
# MAUVAIS - Injection SQL possible
query = f"SELECT * FROM etudiant WHERE id = {user_input}"  # DANGER !

# BON - Requête paramétrée
query = "SELECT * FROM etudiant WHERE id = %s"
cur.execute(query, (user_input,))  # psycopg2 échappe automatiquement
```

**Exemple d'attaque évitée :**
```
user_input = "1; DROP TABLE etudiant; --"

# Version vulnérable exécuterait :
SELECT * FROM etudiant WHERE id = 1; DROP TABLE etudiant; --

# Version paramétrée cherche littéralement :
SELECT * FROM etudiant WHERE id = '1; DROP TABLE etudiant; --'
# → Aucun résultat, pas de suppression
```

---

## 5. Modèles de données (CRUD)

### 5.1 Modèle Étudiant (models/etudiant.py)

```python
from config.database import execute_query

def get_all():
    """Récupère tous les étudiants"""
    return execute_query(
        "SELECT * FROM etudiant ORDER BY nom, prenom",
        fetch=True
    )

def get_by_id(etudiant_id: int):
    """Récupère un étudiant par son ID"""
    return execute_query(
        "SELECT * FROM etudiant WHERE id = %s",
        (etudiant_id,),
        fetch_one=True
    )

def create(nom: str, prenom: str, email: str) -> int:
    """Crée un étudiant et retourne son ID"""
    result = execute_query(
        """INSERT INTO etudiant (nom, prenom, email)
           VALUES (%s, %s, %s)
           RETURNING id""",
        (nom, prenom, email),
        fetch_one=True
    )
    return result['id']

def update(etudiant_id: int, nom: str, prenom: str, email: str):
    """Met à jour un étudiant"""
    execute_query(
        """UPDATE etudiant
           SET nom = %s, prenom = %s, email = %s
           WHERE id = %s""",
        (nom, prenom, email, etudiant_id)
    )

def delete(etudiant_id: int):
    """Supprime un étudiant"""
    execute_query(
        "DELETE FROM etudiant WHERE id = %s",
        (etudiant_id,)
    )

def exists(etudiant_id: int) -> bool:
    """Vérifie si un étudiant existe"""
    result = execute_query(
        "SELECT 1 FROM etudiant WHERE id = %s",
        (etudiant_id,),
        fetch_one=True
    )
    return result is not None

def search(terme: str):
    """Recherche par nom, prénom ou email"""
    pattern = f"%{terme}%"
    return execute_query(
        """SELECT * FROM etudiant
           WHERE nom ILIKE %s OR prenom ILIKE %s OR email ILIKE %s
           ORDER BY nom""",
        (pattern, pattern, pattern),
        fetch=True
    )

def count_emprunts_actifs(etudiant_id: int) -> int:
    """Compte les emprunts en cours d'un étudiant"""
    result = execute_query(
        """SELECT COUNT(*) as count FROM emprunt
           WHERE etudiant_id = %s AND date_retour IS NULL""",
        (etudiant_id,),
        fetch_one=True
    )
    return result['count']
```

### 5.2 Modèle Livre (models/livre.py)

```python
def get_all():
    """Récupère tous les livres"""
    return execute_query(
        "SELECT * FROM livre ORDER BY titre",
        fetch=True
    )

def get_by_id(isbn: str):
    """Récupère un livre par ISBN"""
    return execute_query(
        "SELECT * FROM livre WHERE isbn = %s",
        (isbn,),
        fetch_one=True
    )

def create(titre: str, editeur: str, isbn: str, annee: int = None, exemplaires: int = 1) -> str:
    """Crée un livre"""
    execute_query(
        """INSERT INTO livre (isbn, titre, editeur, annee_publication, exemplaires_dispo)
           VALUES (%s, %s, %s, %s, %s)""",
        (isbn, titre, editeur, annee, exemplaires)
    )
    return isbn

def est_disponible(isbn: str) -> bool:
    """Vérifie si au moins un exemplaire est disponible"""
    result = execute_query(
        "SELECT exemplaires_dispo FROM livre WHERE isbn = %s",
        (isbn,),
        fetch_one=True
    )
    return result and result['exemplaires_dispo'] > 0

def decrementer_exemplaires(isbn: str):
    """Décrémente le nombre d'exemplaires (lors d'un emprunt)"""
    execute_query(
        "UPDATE livre SET exemplaires_dispo = exemplaires_dispo - 1 WHERE isbn = %s",
        (isbn,)
    )

def incrementer_exemplaires(isbn: str):
    """Incrémente le nombre d'exemplaires (lors d'un retour)"""
    execute_query(
        "UPDATE livre SET exemplaires_dispo = exemplaires_dispo + 1 WHERE isbn = %s",
        (isbn,)
    )
```

### 5.3 Modèle Emprunt (models/emprunt.py)

```python
from datetime import date, timedelta

# Constantes métier
DUREE_EMPRUNT_MAX = 14  # jours
TARIF_AMENDE_JOUR = 0.50  # euros

def get_all():
    """Récupère tous les emprunts avec infos étudiant et livre"""
    return execute_query(
        """SELECT e.*,
                  et.nom, et.prenom, et.email,
                  l.titre, l.editeur
           FROM emprunt e
           JOIN etudiant et ON e.etudiant_id = et.id
           JOIN livre l ON e.livre_isbn = l.isbn
           ORDER BY e.date_emprunt DESC""",
        fetch=True
    )

def get_en_cours():
    """Récupère les emprunts non retournés"""
    return execute_query(
        """SELECT e.*,
                  et.nom, et.prenom,
                  l.titre
           FROM emprunt e
           JOIN etudiant et ON e.etudiant_id = et.id
           JOIN livre l ON e.livre_isbn = l.isbn
           WHERE e.date_retour IS NULL
           ORDER BY e.date_emprunt""",
        fetch=True
    )

def get_en_retard():
    """Récupère les emprunts en retard (> 14 jours sans retour)"""
    return execute_query(
        """SELECT e.*,
                  et.nom, et.prenom,
                  l.titre
           FROM emprunt e
           JOIN etudiant et ON e.etudiant_id = et.id
           JOIN livre l ON e.livre_isbn = l.isbn
           WHERE e.date_retour IS NULL
             AND e.date_emprunt < CURRENT_DATE - INTERVAL '14 days'
           ORDER BY e.date_emprunt""",
        fetch=True
    )

def create(etudiant_id: int, livre_isbn: str) -> int:
    """Crée un emprunt et décrémente les exemplaires"""
    from models import livre

    # Créer l'emprunt
    result = execute_query(
        """INSERT INTO emprunt (etudiant_id, livre_isbn)
           VALUES (%s, %s)
           RETURNING id""",
        (etudiant_id, livre_isbn),
        fetch_one=True
    )

    # Décrémenter le stock
    livre.decrementer_exemplaires(livre_isbn)

    return result['id']

def retourner(emprunt_id: int):
    """Marque un emprunt comme retourné"""
    from models import livre

    # Récupérer l'ISBN du livre
    emp = get_by_id(emprunt_id)

    # Mettre à jour la date de retour
    execute_query(
        "UPDATE emprunt SET date_retour = CURRENT_DATE WHERE id = %s",
        (emprunt_id,)
    )

    # Réincrémenter le stock
    livre.incrementer_exemplaires(emp['livre_isbn'])

def calculer_jours_retard(emprunt: dict) -> int:
    """
    Calcule le nombre de jours de retard.
    Retard = date actuelle (ou date retour) - (date emprunt + 14 jours)
    """
    date_emprunt = emprunt['date_emprunt']
    if isinstance(date_emprunt, str):
        date_emprunt = date.fromisoformat(date_emprunt)

    date_limite = date_emprunt + timedelta(days=DUREE_EMPRUNT_MAX)

    # Si retourné, on prend la date de retour, sinon aujourd'hui
    if emprunt['date_retour']:
        date_fin = emprunt['date_retour']
        if isinstance(date_fin, str):
            date_fin = date.fromisoformat(date_fin)
    else:
        date_fin = date.today()

    if date_fin > date_limite:
        return (date_fin - date_limite).days
    return 0

def calculer_amende(emprunt: dict) -> float:
    """Calcule l'amende : 0.50€ par jour de retard"""
    jours = calculer_jours_retard(emprunt)
    return round(jours * TARIF_AMENDE_JOUR, 2)
```

---

## 6. API REST (app.py)

### 6.1 Structure d'une route Flask

```python
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

@app.route('/api/etudiants', methods=['GET'])
def get_etudiants():
    """GET /api/etudiants - Liste tous les étudiants"""
    try:
        etudiants = etudiant.get_all()
        return jsonify(etudiants), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/etudiants/<int:etudiant_id>', methods=['GET'])
def get_etudiant(etudiant_id):
    """GET /api/etudiants/5 - Récupère l'étudiant d'ID 5"""
    try:
        etud = etudiant.get_by_id(etudiant_id)
        if etud:
            return jsonify(etud), 200
        return jsonify({'error': 'Étudiant non trouvé'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/etudiants', methods=['POST'])
def create_etudiant():
    """POST /api/etudiants - Crée un étudiant"""
    try:
        data = request.json  # Corps de la requête en JSON

        # Validation
        nom = valider_non_vide(data.get('nom', ''), 'nom')
        prenom = valider_non_vide(data.get('prenom', ''), 'prénom')
        email = valider_non_vide(data.get('email', ''), 'email')

        if not valider_email(email):
            return jsonify({'error': 'Format email invalide'}), 400

        # Création
        etudiant_id = etudiant.create(nom, prenom, email)
        return jsonify({'id': etudiant_id, 'message': 'Étudiant créé'}), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500
```

### 6.2 Codes HTTP utilisés

| Code | Signification | Utilisation |
|------|---------------|-------------|
| **200** | OK | GET réussi, UPDATE réussi |
| **201** | Created | POST réussi (création) |
| **400** | Bad Request | Données invalides |
| **404** | Not Found | Ressource inexistante |
| **500** | Server Error | Erreur BDD ou serveur |

### 6.3 Endpoints de l'API

**Étudiants**
```
GET    /api/etudiants           → Liste tous les étudiants
GET    /api/etudiants/{id}      → Récupère un étudiant
GET    /api/etudiants/search?q= → Recherche
POST   /api/etudiants           → Crée un étudiant
PUT    /api/etudiants/{id}      → Modifie un étudiant
DELETE /api/etudiants/{id}      → Supprime un étudiant
```

**Livres**
```
GET    /api/livres              → Liste tous les livres
GET    /api/livres/{isbn}       → Récupère un livre
POST   /api/livres              → Crée un livre
PUT    /api/livres/{isbn}       → Modifie un livre
DELETE /api/livres/{isbn}       → Supprime un livre
```

**Emprunts**
```
GET    /api/emprunts            → Liste tous les emprunts
GET    /api/emprunts/en-cours   → Emprunts non retournés
GET    /api/emprunts/en-retard  → Emprunts en retard (> 14j)
POST   /api/emprunts            → Crée un emprunt
POST   /api/emprunts/{id}/retourner → Enregistre un retour
DELETE /api/emprunts/{id}       → Supprime un emprunt
```

**Statistiques**
```
GET    /api/stats/overview      → Vue d'ensemble
GET    /api/stats/top-etudiants → Top 5 emprunteurs
GET    /api/stats/top-livres    → Top 5 livres empruntés
```

---

## 7. Requêtes SQL avancées

### 7.1 Jointures (JOIN)

Pour afficher un emprunt avec les infos de l'étudiant et du livre :

```sql
SELECT e.id, e.date_emprunt, e.date_retour,
       et.nom, et.prenom,       -- Depuis table etudiant
       l.titre, l.editeur       -- Depuis table livre
FROM emprunt e
JOIN etudiant et ON e.etudiant_id = et.id
JOIN livre l ON e.livre_isbn = l.isbn;
```

**Résultat** :
| id | date_emprunt | nom | prenom | titre |
|----|--------------|-----|--------|-------|
| 1 | 2025-01-05 | Martin | Lucas | Le Petit Prince |
| 2 | 2025-01-03 | Dupont | Marie | 1984 |

### 7.2 Agrégations (COUNT, SUM, GROUP BY)

**Top 5 des étudiants qui empruntent le plus :**
```sql
SELECT et.id, et.nom, et.prenom,
       COUNT(e.id) as nb_emprunts
FROM etudiant et
LEFT JOIN emprunt e ON et.id = e.etudiant_id
GROUP BY et.id, et.nom, et.prenom
ORDER BY nb_emprunts DESC
LIMIT 5;
```

**Top 5 des livres les plus empruntés :**
```sql
SELECT l.isbn, l.titre,
       COUNT(e.id) as nb_emprunts
FROM livre l
LEFT JOIN emprunt e ON l.isbn = e.livre_isbn
GROUP BY l.isbn, l.titre
ORDER BY nb_emprunts DESC
LIMIT 5;
```

**Statistiques globales :**
```sql
-- Nombre total d'étudiants
SELECT COUNT(*) FROM etudiant;

-- Nombre d'emprunts en cours
SELECT COUNT(*) FROM emprunt WHERE date_retour IS NULL;

-- Nombre d'emprunts en retard
SELECT COUNT(*) FROM emprunt
WHERE date_retour IS NULL
  AND date_emprunt < CURRENT_DATE - INTERVAL '14 days';
```

### 7.3 Sous-requêtes

**Livres qui n'ont jamais été empruntés :**
```sql
SELECT * FROM livre
WHERE isbn NOT IN (SELECT DISTINCT livre_isbn FROM emprunt);
```

**Étudiants avec plus de 3 emprunts en cours :**
```sql
SELECT et.* FROM etudiant et
WHERE (SELECT COUNT(*) FROM emprunt e
       WHERE e.etudiant_id = et.id AND e.date_retour IS NULL) > 3;
```

### 7.4 Calcul de dates avec INTERVAL

```sql
-- Emprunts de plus de 14 jours
SELECT * FROM emprunt
WHERE date_emprunt < CURRENT_DATE - INTERVAL '14 days'
  AND date_retour IS NULL;

-- Emprunts du dernier mois
SELECT * FROM emprunt
WHERE date_emprunt > CURRENT_DATE - INTERVAL '1 month';
```

---

## 8. Validation et sécurité

### 8.1 Validation des entrées (utils/validators.py)

```python
import re

def valider_email(email: str) -> bool:
    """Vérifie le format d'un email avec une regex"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def valider_non_vide(valeur: str, nom_champ: str) -> str:
    """Vérifie qu'un champ n'est pas vide"""
    if not valeur or not valeur.strip():
        raise ValueError(f"Le champ {nom_champ} est requis")
    return valeur.strip()

def valider_annee(annee_str: str) -> int:
    """Vérifie qu'une année est valide"""
    try:
        annee = int(annee_str)
        if annee < 1000 or annee > date.today().year + 1:
            raise ValueError("Année invalide")
        return annee
    except ValueError:
        raise ValueError("L'année doit être un nombre valide")
```

### 8.2 Gestion des erreurs de contraintes

Quand PostgreSQL refuse une opération (contrainte violée), on traduit l'erreur :

```python
def translateDatabaseError(message: str) -> str:
    """Traduit les erreurs PostgreSQL en messages user-friendly"""

    # Violation d'unicité sur l'email
    if 'etudiant_email_key' in message or 'duplicate' in message:
        return "Cette adresse email est déjà utilisée."

    # Violation de clé étrangère (ON DELETE RESTRICT)
    if 'foreign key' in message:
        return "Impossible de supprimer : des emprunts sont liés."

    # Violation de CHECK
    if 'check' in message.lower():
        return "Valeur invalide (contrainte CHECK violée)."

    return message
```

---

## 9. Règles métier implémentées

### 9.1 Limite d'emprunts

Un étudiant ne peut pas avoir plus de 5 emprunts simultanés :

```python
# Dans app.py, route POST /api/emprunts
nb_emprunts = etudiant.count_emprunts_actifs(etudiant_id)
if nb_emprunts >= 5:
    return jsonify({'error': 'Limite de 5 emprunts atteinte'}), 400
```

### 9.2 Disponibilité des livres

On ne peut emprunter que si `exemplaires_dispo > 0` :

```python
if not livre.est_disponible(isbn):
    return jsonify({'error': 'Livre non disponible'}), 400
```

### 9.3 Gestion du stock

À chaque emprunt/retour, on met à jour le compteur :

```python
# Emprunt → décrémentation
UPDATE livre SET exemplaires_dispo = exemplaires_dispo - 1 WHERE isbn = %s

# Retour → incrémentation
UPDATE livre SET exemplaires_dispo = exemplaires_dispo + 1 WHERE isbn = %s
```

### 9.4 Calcul des amendes

- Durée max : 14 jours
- Amende : 0.50€ par jour de retard
- Calculé dynamiquement (pas stocké en BDD)

```python
def calculer_amende(emprunt):
    jours_retard = calculer_jours_retard(emprunt)
    return jours_retard * 0.50  # €
```

---

## 10. Lancer le projet

### 10.1 Prérequis

```bash
# PostgreSQL installé et lancé
# Python 3.8+ installé
```

### 10.2 Configuration

```bash
cd backend

# Créer le fichier .env
cat > .env << EOF
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bibliotheque
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
EOF
```

### 10.3 Base de données

```bash
# Créer la base
createdb -U postgres bibliotheque

# Créer les tables
psql -U postgres -d bibliotheque -f sql/init.sql

# Insérer des données de test
psql -U postgres -d bibliotheque -f sql/seed.sql
```

### 10.4 Lancer le serveur

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer Flask
python app.py

# → Serveur disponible sur http://localhost:5001
```

### 10.5 Tester l'API

```bash
# Liste des étudiants
curl http://localhost:5001/api/etudiants

# Créer un étudiant
curl -X POST http://localhost:5001/api/etudiants \
  -H "Content-Type: application/json" \
  -d '{"nom": "Dupont", "prenom": "Jean", "email": "jean@test.fr"}'

# Supprimer un étudiant
curl -X DELETE http://localhost:5001/api/etudiants/1
```

---

## 11. Résumé des concepts BDD utilisés

| Concept | Utilisation dans le projet |
|---------|---------------------------|
| **Modélisation relationnelle** | 3 tables avec relations |
| **Clés primaires** | id SERIAL, isbn VARCHAR |
| **Clés étrangères** | emprunt → etudiant, livre |
| **Contraintes UNIQUE** | email unique |
| **Contraintes CHECK** | année valide, dates cohérentes |
| **Contraintes NOT NULL** | champs obligatoires |
| **ON DELETE RESTRICT** | protection intégrité |
| **Index** | optimisation des recherches |
| **Jointures (JOIN)** | affichage emprunt complet |
| **Agrégations** | statistiques, top 5 |
| **Requêtes paramétrées** | protection injection SQL |
| **Transactions** | commit/rollback automatique |

---

**Document préparé pour l'oral - Administration BDD B3 SDV**
**Tom LEFEVRE-BONZON & Ilies MAHOUDEAU**
