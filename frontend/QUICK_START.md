# Demarrage rapide - Bibliotheque App Frontend

## Prérequis
- Node.js 18+ et npm installés
- Backend API démarré sur http://localhost:5001

## Installation et démarrage

```bash
# 1. Installer les dépendances (si ce n'est pas déjà fait)
npm install

# 2. Démarrer le serveur de développement
npm start
```

L'application sera accessible sur **http://localhost:4200**

## Navigation dans l'application

### Etudiants (http://localhost:4200/etudiants)
- Ajouter, modifier, supprimer des étudiants
- Champs: nom, prénom, email

### Livres (http://localhost:4200/livres)
- Gérer le catalogue de livres
- Champs: ISBN, titre, éditeur, année, exemplaires disponibles

### Emprunts (http://localhost:4200/emprunts)
- Créer de nouveaux emprunts
- Filtrer: tous / en cours / en retard
- Retourner des livres (calcul automatique des amendes)

### Statistiques (http://localhost:4200/stats)
- Vue d'ensemble de la bibliothèque
- Top 5 des emprunteurs et livres populaires

## Vérifier la connexion au backend

Si vous voyez l'erreur "Impossible de se connecter au serveur":
1. Vérifiez que le backend est démarré sur le port 5001
2. Testez l'API: `curl http://localhost:5001/api/stats`

## Build de production

```bash
npm run build
```

Les fichiers seront générés dans `dist/frontend/`

## Architecture technique

- **Framework**: Angular 21 (standalone components)
- **UI**: Bootstrap 5 + Bootstrap Icons
- **HTTP**: HttpClient avec RxJS
- **Routing**: Angular Router
- **Forms**: FormsModule (template-driven)

## Fichiers principaux

```
src/app/
├── models/              # Interfaces TypeScript
├── services/            # API service (HTTP calls)
├── components/          # 5 composants (navbar + 4 pages)
├── app.routes.ts        # Configuration du routing
└── app.config.ts        # Configuration globale
```

## Fonctionnalités clés

- Modales Bootstrap pour les formulaires
- Alertes dismissibles pour les messages
- Gestion des erreurs HTTP
- Animations CSS (fade-in)
- Design responsive
- Validation des formulaires
- Confirmations avant suppression

## Aide

Pour plus de détails, consultez le fichier `ANGULAR_APP_README.md`
