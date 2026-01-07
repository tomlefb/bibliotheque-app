# Bibliotheque App - Frontend Angular

Application Angular complète pour la gestion d'une bibliothèque universitaire.

## Structure du projet

```
src/app/
├── components/
│   ├── navbar/          # Barre de navigation
│   ├── etudiants/       # Gestion des étudiants
│   ├── livres/          # Gestion des livres
│   ├── emprunts/        # Gestion des emprunts
│   └── stats/           # Statistiques
├── models/              # Modèles TypeScript
│   ├── etudiant.model.ts
│   ├── livre.model.ts
│   ├── emprunt.model.ts
│   └── stats.model.ts
├── services/
│   └── api.service.ts   # Service HTTP pour l'API
├── app.routes.ts        # Configuration du routing
├── app.config.ts        # Configuration de l'application
└── app.ts/app.html      # Composant racine
```

## Fonctionnalités

### 1. Gestion des étudiants (`/etudiants`)
- Liste des étudiants avec tableau responsive
- Ajout d'un étudiant (modal Bootstrap)
- Modification d'un étudiant
- Suppression avec confirmation
- Validation des champs (nom, prénom, email)

### 2. Gestion des livres (`/livres`)
- Liste des livres avec informations complètes
- Ajout de livre (ISBN, titre, éditeur, année, exemplaires)
- Modification (ISBN non modifiable)
- Suppression avec confirmation
- Badge coloré pour disponibilité

### 3. Gestion des emprunts (`/emprunts`)
- Liste des emprunts avec filtres
  - Tous les emprunts
  - En cours
  - En retard
- Nouvel emprunt (sélection étudiant et livre disponible)
- Retour de livre avec calcul automatique des amendes
- Badges de statut (en cours, retourné, en retard)
- Affichage des amendes

### 4. Statistiques (`/stats`)
- Vue d'ensemble avec 4 cartes
  - Total étudiants
  - Total livres et exemplaires
  - Emprunts en cours
  - Emprunts en retard
- Barre de progression du taux d'emprunt
- Top 5 étudiants emprunteurs
- Top 5 livres populaires
- Bouton d'actualisation

## Configuration

### API Backend
L'application communique avec le backend sur `http://localhost:5001/api`

Configuration dans `/src/app/services/api.service.ts`:
```typescript
private readonly API_URL = 'http://localhost:5001/api';
```

### Routing
Routes configurées dans `/src/app/app.routes.ts`:
- `/` → redirect vers `/etudiants`
- `/etudiants` → EtudiantsComponent
- `/livres` → LivresComponent
- `/emprunts` → EmpruntsComponent
- `/stats` → StatsComponent

## Technologies utilisées

- **Angular 21** (standalone components)
- **Bootstrap 5.3.8** - Framework CSS
- **Bootstrap Icons 1.13.1** - Icônes
- **RxJS** - Programmation réactive
- **HttpClient** - Appels API
- **FormsModule** - Formulaires template-driven

## Design

### Style
- Bootstrap pour le layout et les composants
- Classe `fade-in` pour les animations
- Navbar fixe avec logo et navigation
- Modales Bootstrap pour les formulaires
- Alertes dismissibles pour les messages

### Responsive
- Tables responsive avec `.table-responsive`
- Grid Bootstrap (`.row`, `.col-md-*`)
- Navbar collapsible sur mobile
- Cards adaptatives

## Démarrage

```bash
# Installation des dépendances
npm install

# Lancer le serveur de développement
npm start
# L'app sera accessible sur http://localhost:4200

# Build de production
npm run build
# Les fichiers seront dans dist/frontend
```

## Gestion des erreurs

Le service API gère les erreurs HTTP et affiche des messages appropriés:
- Erreur de connexion au serveur
- Erreurs métier (retournées par le backend)
- Erreurs HTTP (404, 500, etc.)

Les composants affichent les erreurs via des alertes Bootstrap.

## Améliorations possibles

1. Lazy loading des modules
2. Guards pour la protection des routes
3. Intercepteurs HTTP (loading, erreurs globales)
4. Reactive forms au lieu de template-driven
5. NgRx pour la gestion d'état avancée
6. Tests unitaires et e2e
7. PWA (Progressive Web App)
8. i18n (internationalisation)

## Notes

- Les modales utilisent Bootstrap JS (importé dans `main.ts`)
- Les composants sont standalone (pas de modules NgModule)
- HttpClient configuré dans `app.config.ts` via `provideHttpClient()`
- Les styles globaux sont dans `src/styles.scss`
