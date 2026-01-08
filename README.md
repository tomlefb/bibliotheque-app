# Bibliothèque App

Application de gestion de bibliothèque - **Backend Flask + Frontend Angular + PostgreSQL**

---

## Lancement rapide (avec Docker PostgreSQL du cours)

Si vous avez déjà la BDD Docker du cours avec `password` comme mot de passe :

```bash
# 1. Backend
cd backend
pip install -r requirements.txt
python app.py
# → http://localhost:5001

# 2. Frontend (dans un autre terminal)
cd frontend
npm install
npm start
# → http://localhost:4200
```

---

## Installation complète (sans la BDD)

### 1. Base de données PostgreSQL

**Option A - Avec Docker :**
```bash
docker run -d \
  --name postgres-biblio \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:14
```

**Option B - PostgreSQL installé :**
```bash
psql -U postgres
CREATE DATABASE bibliotheque;
\q
```

### 2. Initialiser les tables

```bash
cd backend
psql -U postgres -d bibliotheque -f sql/init.sql
psql -U postgres -d bibliotheque -f sql/seed.sql  # Données de test
```

### 3. Configurer le backend

```bash
cd backend
cp .env.example .env
# Modifier .env si nécessaire (par défaut : password)
```

Contenu du `.env` :
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bibliotheque
DB_USER=postgres
DB_PASSWORD=password
```

### 4. Lancer le backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```
→ API disponible sur **http://localhost:5001**

### 5. Lancer le frontend

```bash
cd frontend
npm install
npm start
```
→ Application disponible sur **http://localhost:4200**

---

## Structure

```
bibliotheque-app/
├── backend/           # API REST Python Flask
│   ├── app.py         # Point d'entrée
│   ├── models/        # CRUD (etudiant, livre, emprunt)
│   ├── services/      # Stats
│   ├── sql/           # Scripts SQL
│   └── .env           # Config BDD
│
└── frontend/          # SPA Angular
    └── src/app/
        ├── components/  # Pages (home, etudiants, livres, emprunts)
        └── services/    # ApiService
```

---

## Fonctionnalités

- CRUD Étudiants / Livres / Emprunts
- Filtres emprunts (tous / en cours / en retard)
- Calcul automatique des amendes (0.50€/jour après 14 jours)
- Limite de 5 emprunts par étudiant
- Statistiques (top étudiants, top livres, taux d'emprunt)

---

## Tech Stack

| Backend | Frontend |
|---------|----------|
| Python 3.x | Angular 21 |
| Flask | TypeScript |
| PostgreSQL | Bootstrap 5 |
| psycopg2 | RxJS |

---

## Auteurs

**Tom LEFEVRE-BONZON & Ilies MAHOUDEAU** - B3 Dev SDV
