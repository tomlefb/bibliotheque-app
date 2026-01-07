# Rapport de Projet - Application de Gestion de Bibliothèque

**Module** : Administration de Bases de Données
**Formation** : B3 Développement - SDV
**Année universitaire** : 2025-2026
**Auteurs** : Tom LEFEVRE-BONZON & Ilies MAHOUDEAU

---

## Table des matières

1. [Introduction](#1-introduction)
2. [Architecture du projet](#2-architecture-du-projet)
3. [Partie Backend](#3-partie-backend)
4. [Partie Frontend](#4-partie-frontend)
5. [Base de données](#5-base-de-données)
6. [Fonctionnalités implémentées](#6-fonctionnalités-implémentées)
7. [Sécurité et robustesse](#7-sécurité-et-robustesse)
8. [Guide d'installation](#8-guide-dinstallation)
9. [Conclusion](#9-conclusion)

---

## 1. Introduction

### 1.1 Contexte

Dans le cadre du module d'Administration de Bases de Données, nous avons développé une application complète de gestion de bibliothèque universitaire. Ce projet met en pratique les concepts de conception de bases de données relationnelles, de développement Python et d'architecture applicative orientée données.

### 1.2 Objectifs

L'objectif principal était de créer une application permettant de :
- Gérer un catalogue de livres
- Gérer les étudiants inscrits à la bibliothèque
- Suivre les emprunts et retours de livres
- Calculer automatiquement les retards et amendes

### 1.3 Choix techniques

Nous avons fait le choix d'aller au-delà d'un simple menu interactif en console pour proposer une architecture moderne client-serveur :
- **Backend** : API REST en Python avec Flask
- **Frontend** : Application web avec Angular
- **Base de données** : PostgreSQL

Ce choix permet une meilleure séparation des responsabilités et une expérience utilisateur plus agréable.

---

## 2. Architecture du projet

```
bibliotheque-app/
├── backend/                    # API Python Flask
│   ├── app.py                 # Point d'entrée de l'API
│   ├── config/
│   │   ├── database.py        # Connexion PostgreSQL
│   │   └── settings.py        # Configuration
│   ├── models/
│   │   ├── etudiant.py        # Modèle Étudiant
│   │   ├── livre.py           # Modèle Livre
│   │   └── emprunt.py         # Modèle Emprunt
│   ├── services/
│   │   └── stats_service.py   # Service statistiques
│   ├── utils/
│   │   ├── validators.py      # Validation des données
│   │   ├── formatters.py      # Formatage
│   │   └── logger.py          # Journalisation
│   └── sql/
│       ├── init.sql           # Script création tables
│       └── seed.sql           # Données de test
│
└── frontend/                   # Application Angular
    └── src/app/
        ├── components/        # Composants UI
        ├── services/          # Services HTTP
        └── models/            # Interfaces TypeScript
```

Cette architecture suit le pattern MVC (Modèle-Vue-Contrôleur) avec une séparation claire entre :
- Les **modèles** qui gèrent l'accès aux données
- Les **contrôleurs** (routes Flask) qui traitent les requêtes
- Les **vues** (composants Angular) qui affichent l'interface

---

## 3. Partie Backend

### 3.1 Technologies utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| Python | 3.x | Langage principal |
| Flask | 3.x | Framework web |
| psycopg2 | 2.9.x | Driver PostgreSQL |
| Flask-CORS | 5.x | Gestion des requêtes cross-origin |

### 3.2 Structure de l'API REST

L'API expose les endpoints suivants :

**Étudiants** (`/api/etudiants`)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/etudiants` | Liste tous les étudiants |
| GET | `/api/etudiants/{id}` | Récupère un étudiant |
| POST | `/api/etudiants` | Crée un étudiant |
| PUT | `/api/etudiants/{id}` | Modifie un étudiant |
| DELETE | `/api/etudiants/{id}` | Supprime un étudiant |

**Livres** (`/api/livres`)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/livres` | Liste tous les livres |
| GET | `/api/livres/{isbn}` | Récupère un livre |
| POST | `/api/livres` | Crée un livre |
| PUT | `/api/livres/{isbn}` | Modifie un livre |
| DELETE | `/api/livres/{isbn}` | Supprime un livre |

**Emprunts** (`/api/emprunts`)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/emprunts` | Liste tous les emprunts |
| GET | `/api/emprunts/en-cours` | Emprunts non retournés |
| GET | `/api/emprunts/en-retard` | Emprunts en retard |
| POST | `/api/emprunts` | Crée un emprunt |
| POST | `/api/emprunts/{id}/retourner` | Marque un retour |
| DELETE | `/api/emprunts/{id}` | Supprime un emprunt |

**Statistiques** (`/api/stats`)
| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/stats/overview` | Vue d'ensemble |
| GET | `/api/stats/top-etudiants` | Top 5 emprunteurs |
| GET | `/api/stats/top-livres` | Top 5 livres empruntés |

### 3.3 Gestion de la base de données

La connexion à PostgreSQL est centralisée dans `config/database.py`. Nous utilisons un pattern de connexion sécurisé avec :

```python
def execute_query(query: str, params: tuple = None, fetch: bool = False):
    """Exécute une requête SQL de manière sécurisée."""
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)  # Requête paramétrée
            if fetch:
                return cur.fetchall()
            conn.commit()
```

Les requêtes sont **toujours paramétrées** pour éviter les injections SQL.

### 3.4 Modèles de données

Chaque entité dispose de son propre module avec les opérations CRUD :

**Exemple - etudiant.py** :
```python
def get_all():
    """Récupère tous les étudiants"""
    return execute_query("SELECT * FROM etudiant ORDER BY nom", fetch=True)

def create(nom: str, prenom: str, email: str) -> int:
    """Crée un nouvel étudiant"""
    result = execute_query(
        "INSERT INTO etudiant (nom, prenom, email) VALUES (%s, %s, %s) RETURNING id",
        (nom, prenom, email),
        fetch_one=True
    )
    return result['id']
```

### 3.5 Règles métier implémentées

Le backend applique plusieurs règles métier :

1. **Limite d'emprunts** : Un étudiant ne peut pas avoir plus de 5 emprunts simultanés
2. **Disponibilité** : On ne peut emprunter que des livres disponibles
3. **Calcul des retards** : Durée d'emprunt maximale de 14 jours
4. **Calcul des amendes** : 0.50€ par jour de retard

```python
def calculer_jours_retard(emprunt: dict) -> int:
    """Calcule le nombre de jours de retard"""
    DUREE_EMPRUNT_MAX = 14
    date_limite = emprunt['date_emprunt'] + timedelta(days=DUREE_EMPRUNT_MAX)
    date_fin = emprunt['date_retour'] or date.today()

    if date_fin > date_limite:
        return (date_fin - date_limite).days
    return 0

def calculer_amende(emprunt: dict) -> float:
    """Calcule l'amende (0.50€ par jour de retard)"""
    TARIF_JOUR = 0.50
    jours = calculer_jours_retard(emprunt)
    return round(jours * TARIF_JOUR, 2)
```

---

## 4. Partie Frontend

### 4.1 Technologies utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| Angular | 21.x | Framework frontend |
| TypeScript | 5.x | Langage typé |
| Bootstrap | 5.3 | Framework CSS |
| Bootstrap Icons | 1.x | Icônes |

### 4.2 Architecture des composants

L'application utilise les **standalone components** d'Angular (nouvelle approche recommandée) :

```
src/app/
├── components/
│   ├── home/              # Page d'accueil avec statistiques
│   ├── etudiants/         # Gestion des étudiants
│   ├── livres/            # Gestion des livres
│   ├── emprunts/          # Gestion des emprunts
│   └── shared/
│       └── confirm-modal/ # Modal de confirmation réutilisable
├── services/
│   └── api.service.ts     # Communication avec le backend
└── models/
    ├── etudiant.model.ts
    ├── livre.model.ts
    └── emprunt.model.ts
```

### 4.3 Service API

Le service `ApiService` centralise toutes les communications HTTP :

```typescript
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly API_URL = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  // Exemple : récupération des étudiants
  getEtudiants(): Observable<Etudiant[]> {
    return this.http.get<Etudiant[]>(`${this.API_URL}/etudiants`)
      .pipe(catchError(this.handleError));
  }

  // Gestion centralisée des erreurs
  private handleError = (error: HttpErrorResponse) => {
    let errorMessage = 'Une erreur est survenue';

    if (error.error?.error) {
      errorMessage = this.translateDatabaseError(error.error.error);
    }

    return throwError(() => new Error(errorMessage));
  }
}
```

### 4.4 Interfaces utilisateur

Chaque section dispose d'une interface complète avec :

- **Tableau de données** avec affichage paginé
- **Formulaires** de création/modification dans des modals Bootstrap
- **Filtres et recherche** (notamment pour les emprunts)
- **Messages de confirmation** pour les suppressions
- **Alertes** de succès/erreur avec auto-dismiss

### 4.5 Gestion des erreurs côté client

Les erreurs de la base de données sont traduites en messages compréhensibles :

```typescript
private translateDatabaseError(message: string): string {
  if (message.includes('etudiant_email_key')) {
    return 'Cette adresse email est déjà utilisée par un autre étudiant.';
  }
  if (message.includes('livre_pkey')) {
    return 'Ce numéro ISBN existe déjà dans la base de données.';
  }
  if (message.includes('foreign key')) {
    return 'Impossible de supprimer : des emprunts sont associés à cet élément.';
  }
  return message;
}
```

---

## 5. Base de données

### 5.1 Modèle conceptuel

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  ETUDIANT   │       │   EMPRUNT   │       │    LIVRE    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ id (PK)     │──┐    │ id (PK)     │    ┌──│ isbn (PK)   │
│ nom         │  └───>│ etudiant_id │    │  │ titre       │
│ prenom      │       │ livre_id    │<───┘  │ editeur     │
│ email (UQ)  │       │ date_emprunt│       │ annee       │
│ created_at  │       │ date_retour │       │ exemplaires │
└─────────────┘       │ created_at  │       │ created_at  │
                      └─────────────┘       └─────────────┘
```

### 5.2 Script de création

```sql
-- Table etudiant
CREATE TABLE etudiant (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table livre
CREATE TABLE livre (
    isbn VARCHAR(20) PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    editeur VARCHAR(200) NOT NULL,
    annee_publication INTEGER,
    exemplaires_dispo INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (annee_publication IS NULL OR
           annee_publication BETWEEN 1000 AND EXTRACT(YEAR FROM CURRENT_DATE))
);

-- Table emprunt
CREATE TABLE emprunt (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiant(id) ON DELETE RESTRICT,
    livre_isbn VARCHAR(20) NOT NULL REFERENCES livre(isbn) ON DELETE RESTRICT,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (date_retour IS NULL OR date_retour >= date_emprunt)
);
```

### 5.3 Contraintes d'intégrité

| Contrainte | Table | Description |
|------------|-------|-------------|
| PRIMARY KEY | Toutes | Identifiant unique |
| FOREIGN KEY | emprunt | Liens vers etudiant et livre |
| UNIQUE | etudiant.email | Pas de doublons d'email |
| CHECK | livre | Année valide |
| CHECK | emprunt | Date retour >= date emprunt |
| ON DELETE RESTRICT | emprunt | Empêche suppression si emprunts liés |

### 5.4 Index

Des index ont été créés pour optimiser les requêtes fréquentes :

```sql
CREATE INDEX idx_etudiant_nom ON etudiant(nom);
CREATE INDEX idx_etudiant_email ON etudiant(email);
CREATE INDEX idx_livre_titre ON livre(titre);
CREATE INDEX idx_emprunt_etudiant ON emprunt(etudiant_id);
CREATE INDEX idx_emprunt_livre ON emprunt(livre_isbn);
CREATE INDEX idx_emprunt_date_retour ON emprunt(date_retour);
```

---

## 6. Fonctionnalités implémentées

### 6.1 Gestion des étudiants
- Affichage de la liste complète
- Ajout d'un nouvel étudiant
- Modification des informations
- Suppression (avec vérification des emprunts liés)

### 6.2 Gestion des livres
- Catalogue complet avec ISBN, titre, éditeur, année
- Gestion du nombre d'exemplaires disponibles
- Badge visuel indiquant la disponibilité

### 6.3 Gestion des emprunts
- Création d'emprunt avec sélection étudiant/livre
- Filtrage : tous / en cours / en retard
- Recherche par nom d'étudiant ou titre de livre
- Enregistrement des retours
- Calcul automatique des jours de retard
- Calcul automatique des amendes

### 6.4 Tableau de bord statistiques
- Nombre total d'étudiants, livres, emprunts
- Emprunts en cours et en retard
- Total des amendes
- Taux d'emprunt (livres empruntés / total)
- Top 5 des étudiants les plus actifs
- Top 5 des livres les plus empruntés

---

## 7. Sécurité et robustesse

### 7.1 Protection contre les injections SQL

Toutes les requêtes utilisent des **paramètres placeholders** :

```python
# Correct - Requête paramétrée
cur.execute("SELECT * FROM etudiant WHERE id = %s", (id,))

# Jamais - Concaténation de chaînes
cur.execute(f"SELECT * FROM etudiant WHERE id = {id}")  # DANGER
```

### 7.2 Validation des entrées

Les données sont validées avant insertion :

```python
def valider_email(email: str) -> bool:
    """Vérifie le format de l'email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def valider_non_vide(valeur: str, nom_champ: str) -> str:
    """Vérifie qu'un champ n'est pas vide"""
    if not valeur or not valeur.strip():
        raise ValueError(f"Le champ {nom_champ} est requis")
    return valeur.strip()
```

### 7.3 Gestion des erreurs

- Logging centralisé des erreurs
- Messages d'erreur explicites pour l'utilisateur
- Codes HTTP appropriés (400, 404, 500)
- Auto-dismiss des alertes après délai

### 7.4 Contraintes de la base

La base de données elle-même assure l'intégrité :
- Unicité des emails (contrainte UNIQUE)
- Cohérence des dates (contrainte CHECK)
- Intégrité référentielle (FOREIGN KEY avec RESTRICT)

---

## 8. Guide d'installation

### 8.1 Prérequis

- Python 3.8+
- Node.js 18+
- PostgreSQL 14+

### 8.2 Installation du backend

```bash
cd backend

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Configurer la base de données
cp .env.example .env
# Éditer .env avec vos paramètres PostgreSQL

# Créer les tables
psql -U postgres -d bibliotheque -f sql/init.sql
psql -U postgres -d bibliotheque -f sql/seed.sql  # Données de test

# Lancer le serveur
python app.py
```

### 8.3 Installation du frontend

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de développement
npm start
```

### 8.4 Accès à l'application

- **Frontend** : http://localhost:4200
- **API Backend** : http://localhost:5001/api

---

## 9. Conclusion

### 9.1 Bilan

Ce projet nous a permis de mettre en pratique l'ensemble des compétences du module :

- **Conception de base de données** : Modélisation relationnelle, contraintes, index
- **SQL avancé** : Jointures, agrégations, requêtes paramétrées
- **Développement Python** : Architecture modulaire, gestion d'erreurs, API REST
- **Développement applicatif** : Interface utilisateur complète et ergonomique

### 9.2 Difficultés rencontrées

- Gestion du contexte `this` en TypeScript pour les callbacks
- Synchronisation des modals Bootstrap avec Angular
- Traduction des erreurs PostgreSQL en messages utilisateur

### 9.3 Améliorations possibles

- Authentification des utilisateurs
- Historique des modifications
- Export des données en CSV/PDF
- Notifications par email pour les retards
- Application mobile

---

**Projet réalisé par Tom LEFEVRE-BONZON & Ilies MAHOUDEAU - B3 Dev SDV**
