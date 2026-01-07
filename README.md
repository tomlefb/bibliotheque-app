# Bibliothèque Universitaire - Application de Gestion

Application complète de gestion de bibliothèque universitaire avec interface web moderne et CLI Python + PostgreSQL.

## Fonctionnalités

### CRUD Complet
- **Étudiants** : Créer, Lister, Rechercher, Modifier, Supprimer
- **Livres** : Créer, Lister, Rechercher, Modifier, Supprimer
- **Emprunts** : Créer, Lister (tous/en cours/en retard), Retourner, Supprimer

### Fonctionnalités Métier
- Gestion des emprunts avec validation (disponibilité livre, limite par étudiant)
- Calcul automatique des retards et amendes (0.50€/jour)
- Emprunts limités à 5 par étudiant
- Durée d'emprunt par défaut : 14 jours

### Statistiques
- Vue d'ensemble (totaux, taux d'emprunt)
- Top 5 étudiants (plus d'emprunts)
- Top 5 livres (plus empruntés)
- Liste des emprunts en retard avec amendes

## Stack Technique

### Backend
- **Python** 3.14+
- **Flask** (API REST + serveur web)
- **PostgreSQL** (base de données)
- **psycopg2-binary** (driver PostgreSQL)
- **python-dotenv** (variables d'environnement)

### Frontend
- **HTML5** / **CSS3**
- **Bootstrap 5** (framework UI)
- **JavaScript** vanilla (fetch API, DOM manipulation)
- **Bootstrap Icons**

## Structure du Projet

```
bibliotheque-app/
├── main.py                 # Point d'entrée CLI
├── app.py                  # Serveur Flask + API REST
├── templates/
│   └── index.html          # Interface web
├── static/
│   ├── css/
│   │   └── style.css       # Styles custom
│   └── js/
│       └── app.js          # Logique frontend
├── config/
│   ├── database.py         # Connexion BDD + requêtes sécurisées
│   └── settings.py         # Constantes de l'application
├── models/
│   ├── etudiant.py         # CRUD Etudiant
│   ├── livre.py            # CRUD Livre
│   └── emprunt.py          # CRUD Emprunt + calculs amendes
├── services/
│   └── stats_service.py    # Statistiques et agrégations
├── utils/
│   ├── validators.py       # Validation des inputs
│   ├── formatters.py       # Formatage affichage console
│   └── logger.py           # Logging simple
├── views/
│   ├── menu.py             # Menu principal
│   ├── etudiant_view.py    # Interface étudiants
│   ├── livre_view.py       # Interface livres
│   ├── emprunt_view.py     # Interface emprunts
│   └── stats_view.py       # Interface statistiques
├── sql/
│   ├── init.sql            # Création des tables
│   └── seed.sql            # Données de test
├── .env.example            # Template variables d'environnement
├── requirements.txt        # Dépendances Python
└── README.md
```

## Installation

### 1. Prérequis

- Python 3.14+ installé
- PostgreSQL installé et démarré
- Git (optionnel)

### 2. Cloner le projet

```bash
git clone <url-du-repo>
cd bibliotheque-app
```

### 3. Créer un environnement virtuel

```bash
python -m venv venv

# Activer l'environnement
# Sur macOS/Linux:
source venv/bin/activate

# Sur Windows:
venv\Scripts\activate
```

### 4. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 5. Configuration de la base de données

#### a. Créer le fichier .env

```bash
cp .env.example .env
```

Modifier `.env` avec vos paramètres PostgreSQL :

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bibliotheque
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
```

#### b. Créer la base de données

Se connecter à PostgreSQL :

```bash
psql -U postgres
```

Créer la base :

```sql
CREATE DATABASE bibliotheque;
\q
```

#### c. Initialiser les tables

```bash
psql -U postgres -d bibliotheque -f sql/init.sql
```

#### d. Insérer les données de test (optionnel)

```bash
psql -U postgres -d bibliotheque -f sql/seed.sql
```

## Utilisation

### Option 1 : Interface Web (recommandé)

Lancer le serveur Flask :

```bash
python app.py
```

Ouvrir le navigateur : **http://localhost:5000**

L'interface web offre :
- Navigation par onglets (Étudiants, Livres, Emprunts, Statistiques)
- Recherche en temps réel
- Modales pour ajouter/modifier
- Tableaux interactifs
- Design responsive et moderne

### Option 2 : Interface CLI

```bash
python main.py
```

### Navigation dans les menus

L'application propose une navigation par menus numérotés :

```
========================================
GESTION BIBLIOTHEQUE UNIVERSITAIRE
========================================
  1. Gérer les étudiants
  2. Gérer les livres
  3. Gérer les emprunts
  4. Statistiques
  5. Quitter
========================================
Choix:
```

Entrez le numéro de votre choix et validez avec Entrée.

### Exemples d'opérations

#### Interface Web

**Ajouter un étudiant :**
1. Onglet "Étudiants"
2. Cliquer "Ajouter"
3. Remplir le formulaire
4. Cliquer "Enregistrer"

**Créer un emprunt :**
1. Onglet "Emprunts"
2. Cliquer "Nouvel emprunt"
3. Saisir ID étudiant et ID livre
4. Cliquer "Créer"

**Retourner un livre :**
1. Onglet "Emprunts"
2. Cliquer sur l'icône verte ✓ dans la ligne de l'emprunt
3. L'amende éventuelle est affichée

#### Interface CLI

**Ajouter un étudiant :**
1. Menu principal → `1`
2. Gérer les étudiants → `4`
3. Saisir nom, prénom, email

## Sécurité

### Points d'attention implémentés

- **Variables d'environnement** : Credentials BDD stockés dans `.env` (non versionné)
- **Requêtes paramétrées** : 100% des requêtes SQL utilisent des placeholders `%s`
- **Validation des inputs** : Tous les inputs utilisateur sont validés avant traitement
- **Gestionnaires de contexte** : Utilisation de `with` pour toutes les connexions BDD
- **Gestion d'erreurs** : Try/except avec rollback sur toutes les opérations critiques
- **Contraintes d'intégrité** : Foreign keys, checks, et validations au niveau BDD

### Bonnes pratiques

- Pas de concaténation SQL (protection contre injection SQL)
- Fermeture automatique des connexions
- Logging des erreurs
- Messages d'erreur clairs pour l'utilisateur
- Confirmation avant suppression

## Architecture

### Principes de développement

- **KISS** : Code simple et direct
- **Fonctions pures** : Pas de classes inutiles
- **Séparation des responsabilités** : Modèles / Services / Vues
- **Type hints** : Pour la clarté du code
- **Docstrings** : Documentation en français

### Couches applicatives

1. **Models** : Opérations CRUD sur la base de données
2. **Services** : Logique métier et calculs
3. **Views** : Interface utilisateur (menus, affichage)
4. **Utils** : Fonctions utilitaires (validation, formatage, logging)
5. **Config** : Configuration BDD et constantes

## Schéma de Base de Données

```sql
etudiant
├── id (PK)
├── nom
├── prenom
├── email (UNIQUE)
└── created_at

livre
├── id (PK)
├── titre
├── auteur
├── annee_publication
└── created_at

emprunt
├── id (PK)
├── etudiant_id (FK → etudiant.id)
├── livre_id (FK → livre.id)
├── date_emprunt
├── date_retour (NULL si en cours)
└── created_at
```

## Tests

L'application peut être testée avec les données de test fournies dans `sql/seed.sql` qui contient :
- 10 étudiants
- 25 livres (classiques, SF, tech, etc.)
- Emprunts en cours, en retard, et terminés

## Logs

Les opérations importantes sont enregistrées dans `app.log` :
- Démarrage/arrêt de l'application
- Erreurs de connexion BDD
- Erreurs SQL

## Troubleshooting

### Erreur de connexion PostgreSQL

```
Vérifiez que PostgreSQL est démarré
Vérifiez les credentials dans .env
Testez: psql -U postgres -d bibliotheque
```

### Import errors

```bash
# Vérifier que l'environnement virtuel est activé
which python  # doit pointer vers venv/bin/python

# Réinstaller les dépendances
pip install -r requirements.txt
```

### Table déjà existe

```bash
# Réinitialiser la base
psql -U postgres -d bibliotheque -f sql/init.sql
```

## Auteur

Projet développé pour le Bachelor 3 - Administration de Base de Données - Sup de Vinci

## Licence

Projet académique
