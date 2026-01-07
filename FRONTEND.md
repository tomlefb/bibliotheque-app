# Documentation Frontend

## Architecture

Le frontend est construit avec une approche KISS (Keep It Simple, Stupid) :
- Pas de framework JS lourd (React, Vue, Angular)
- HTML/CSS/JavaScript vanilla
- Bootstrap 5 pour le design
- Fetch API pour les appels REST

## Structure

```
templates/
└── index.html          # Page unique (SPA simple)

static/
├── css/
│   └── style.css       # Styles custom
└── js/
    └── app.js          # Logique application
```

## Fonctionnement

### 1. Page Unique avec Onglets

L'application utilise les **Bootstrap Tabs** pour une navigation fluide :
- Étudiants
- Livres
- Emprunts
- Statistiques

### 2. Communication avec l'API

Toutes les opérations passent par l'API REST Flask (`/api/*`) :

```javascript
// Exemple : Récupérer tous les étudiants
async function loadEtudiants() {
    const etudiants = await apiRequest('/etudiants');
    displayEtudiants(etudiants);
}
```

### 3. Modales Bootstrap

Les formulaires d'ajout/modification utilisent des **modales Bootstrap** :
- `etudiantModal` : Ajouter/modifier un étudiant
- `livreModal` : Ajouter/modifier un livre
- `empruntModal` : Créer un emprunt

### 4. Gestion d'Erreurs

```javascript
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_URL}${endpoint}`, options);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Erreur serveur');
        }

        return data;
    } catch (error) {
        showAlert(error.message, 'danger');
        throw error;
    }
}
```

### 5. Notifications

Système d'alertes Bootstrap pour le feedback utilisateur :

```javascript
function showAlert(message, type = 'success') {
    // Affiche une alerte Bootstrap
    // Auto-dismiss après 5 secondes
}
```

## Routes API Utilisées

### Étudiants
- `GET /api/etudiants` - Liste tous
- `GET /api/etudiants/:id` - Détails
- `GET /api/etudiants/search?q=terme` - Recherche
- `POST /api/etudiants` - Créer
- `PUT /api/etudiants/:id` - Modifier
- `DELETE /api/etudiants/:id` - Supprimer

### Livres
- `GET /api/livres` - Liste tous
- `GET /api/livres/:id` - Détails
- `GET /api/livres/search?q=terme` - Recherche
- `POST /api/livres` - Créer
- `PUT /api/livres/:id` - Modifier
- `DELETE /api/livres/:id` - Supprimer

### Emprunts
- `GET /api/emprunts` - Liste tous
- `GET /api/emprunts/en-cours` - En cours uniquement
- `GET /api/emprunts/en-retard` - En retard uniquement
- `POST /api/emprunts` - Créer
- `POST /api/emprunts/:id/retourner` - Retourner un livre
- `DELETE /api/emprunts/:id` - Supprimer

### Statistiques
- `GET /api/stats/overview` - Vue d'ensemble
- `GET /api/stats/top-etudiants` - Top 5 étudiants
- `GET /api/stats/top-livres` - Top 5 livres

## Design Pattern

### Flux de Données

```
User Action → Event Handler → API Request → Update DOM
```

Exemple pour ajouter un étudiant :

```
1. Clic sur "Ajouter" → showAddEtudiantModal()
2. Remplir formulaire
3. Clic "Enregistrer" → saveEtudiant()
4. saveEtudiant() → fetch POST /api/etudiants
5. Succès → loadEtudiants() → displayEtudiants()
```

### Séparation des Responsabilités

```javascript
// Chargement des données
async function loadEtudiants() { ... }

// Affichage des données
function displayEtudiants(etudiants) { ... }

// Actions utilisateur
async function saveEtudiant() { ... }
async function deleteEtudiant(id) { ... }
```

## Styles Custom

Le fichier `style.css` contient :
- Variables CSS (couleurs)
- Styles pour les tableaux
- Cartes de statistiques
- Animations et transitions
- Responsive design

### Exemple de Carte Statistique

```css
.stat-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    transition: transform 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-3px);
}
```

## Responsive Design

Bootstrap gère automatiquement le responsive avec sa grille :

```html
<div class="row">
    <div class="col-md-6">Colonne 1</div>
    <div class="col-md-6">Colonne 2</div>
</div>
```

- Mobile (< 768px) : 1 colonne
- Tablet (≥ 768px) : 2 colonnes
- Desktop (≥ 992px) : Layout complet

## Performance

### Optimisations
- Pas de framework JS lourd
- CDN pour Bootstrap (cache navigateur)
- Chargement lazy des stats (au clic sur l'onglet)
- Animations CSS (GPU accelerated)

### Bundle Size
- HTML : ~10KB
- CSS : ~5KB
- JS : ~10KB
- **Total : ~25KB** (hors Bootstrap CDN)

## Extension Future

Pour ajouter une nouvelle fonctionnalité :

1. **Ajouter une route API** dans `app.py`
2. **Créer les fonctions JS** dans `app.js`
3. **Ajouter l'UI** dans `index.html`
4. **Styler si nécessaire** dans `style.css`

### Exemple : Ajouter une recherche avancée

```javascript
// 1. Créer la fonction de recherche
async function searchAvancee(filters) {
    const params = new URLSearchParams(filters);
    const results = await apiRequest(`/livres/search-advanced?${params}`);
    displayLivres(results);
}

// 2. Ajouter l'event listener
document.getElementById('searchBtn').addEventListener('click', () => {
    const filters = {
        titre: document.getElementById('filterTitre').value,
        auteur: document.getElementById('filterAuteur').value,
        annee: document.getElementById('filterAnnee').value
    };
    searchAvancee(filters);
});
```

## Bonnes Pratiques Appliquées

### JavaScript
- Async/await pour les appels API
- Try/catch pour la gestion d'erreurs
- Fonctions pures et réutilisables
- Nommage explicite en français

### HTML
- Sémantique HTML5
- Accessibilité (labels, aria-*)
- Validation des formulaires

### CSS
- Variables CSS pour les couleurs
- Mobile-first avec Bootstrap
- Transitions pour UX fluide
- Classes utilitaires Bootstrap

## Débogage

### Console Browser
```javascript
// Tous les logs d'erreur sont dans la console
console.error('Erreur chargement étudiants:', error);
```

### Network Tab
- Voir toutes les requêtes API
- Inspecter les réponses
- Temps de chargement

### Bootstrap DevTools
- Vérifier les classes appliquées
- Tester le responsive
- Déboguer les modales

## Conclusion

Cette architecture frontend est :
- **Simple** : Pas de build system, pas de transpilation
- **Efficace** : Chargement rapide, peu de dépendances
- **Maintenable** : Code clair et structuré
- **Extensible** : Facile d'ajouter des fonctionnalités

Parfait pour un projet académique qui doit rester compréhensible et professionnel.
