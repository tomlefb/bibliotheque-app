# Guide de Démarrage Rapide

## Installation en 5 minutes

### 1. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 2. Initialiser la base de données

```bash
# Créer la base (si pas déjà fait)
createdb bibliotheque

# Créer les tables
psql -U postgres -d bibliotheque -f sql/init.sql

# Insérer les données de test
psql -U postgres -d bibliotheque -f sql/seed.sql
```

### 3. Lancer l'application web

```bash
python app.py
```

Ouvrir **http://localhost:5000** dans votre navigateur.

**C'est tout !** L'application est prête à l'emploi.

## Accès Rapide

### Interface Web
```
http://localhost:5000
```

### Données de Test
- **10 étudiants** déjà créés
- **25 livres** dans le catalogue
- **Emprunts** en cours, en retard, et terminés

## Opérations de Base

### Ajouter un étudiant
1. Onglet "Étudiants"
2. Bouton "Ajouter"
3. Remplir : nom, prénom, email
4. Sauvegarder

### Emprunter un livre
1. Onglet "Emprunts"
2. Bouton "Nouvel emprunt"
3. Saisir : ID étudiant, ID livre
4. Créer

### Retourner un livre
1. Onglet "Emprunts"
2. Clic sur l'icône ✓ verte
3. L'amende s'affiche si retard

### Voir les statistiques
1. Onglet "Statistiques"
2. Vue d'ensemble + Top 5

## Troubleshooting Express

### Erreur de connexion BDD
```bash
# Vérifier que PostgreSQL tourne
pg_isready

# Vérifier les credentials dans .env
cat .env
```

### Port 5000 déjà utilisé
```bash
# Modifier le port dans app.py (ligne finale)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Erreur d'import
```bash
# Vérifier l'environnement virtuel
which python  # doit pointer vers venv/

# Réinstaller
pip install -r requirements.txt
```

## Passer en Production

### Désactiver le mode debug

Dans `app.py`, ligne finale :
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

### Utiliser un vrai serveur WSGI

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Architecture Simplifiée

```
User Browser
    ↓
Flask (app.py)
    ↓
Models (etudiant, livre, emprunt)
    ↓
PostgreSQL Database
```

## Commandes Utiles

```bash
# Réinitialiser la BDD
psql -U postgres -d bibliotheque -f sql/init.sql
psql -U postgres -d bibliotheque -f sql/seed.sql

# Voir les logs
tail -f app.log

# Lancer en mode CLI
python main.py

# Vérifier la connexion BDD
python -c "from config.database import test_connection; print(test_connection())"
```

## Données de Test - IDs Utiles

### Étudiants (IDs 1-10)
- ID 1 : Jean Dupont
- ID 2 : Sophie Martin
- ID 3 : Luc Bernard

### Livres (IDs 1-25)
- ID 1 : Le Petit Prince
- ID 6 : 1984
- ID 11 : Harry Potter

### Emprunts
- En cours : 3-8
- En retard : quelques-uns
- Terminés : 10+

## Support

- README.md : Documentation complète
- FRONTEND.md : Architecture frontend
- Code commenté en français
- Logs dans `app.log`

Bonne utilisation !
