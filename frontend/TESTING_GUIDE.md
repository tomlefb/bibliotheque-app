# Guide de test - Bibliotheque App Frontend

## Préparation

1. Démarrer le backend API sur le port 5001
2. Démarrer le frontend: `npm start`
3. Ouvrir http://localhost:4200 dans le navigateur

## Tests manuels à effectuer

### 1. Test de la navigation

- La page devrait rediriger automatiquement vers `/etudiants`
- Cliquer sur chaque lien de la navbar:
  - Etudiants (devrait être actif en bleu)
  - Livres
  - Emprunts
  - Statistiques
- Vérifier que l'icône et le titre correspondent à chaque page

### 2. Test Etudiants

#### Ajout
1. Cliquer sur "Ajouter un étudiant"
2. Remplir le formulaire:
   - Nom: Dupont
   - Prénom: Jean
   - Email: jean.dupont@example.com
3. Cliquer sur "Ajouter"
4. Vérifier:
   - Message de succès vert
   - Étudiant apparaît dans le tableau
   - Modal se ferme automatiquement

#### Validation
1. Ouvrir la modal d'ajout
2. Essayer de soumettre avec des champs vides
3. Vérifier le message d'erreur rouge

#### Modification
1. Cliquer sur l'icône crayon d'un étudiant
2. Modifier le nom
3. Cliquer sur "Modifier"
4. Vérifier la mise à jour dans le tableau

#### Suppression
1. Cliquer sur l'icône poubelle
2. Confirmer la suppression
3. Vérifier la disparition de l'étudiant

### 3. Test Livres

#### Ajout
1. Cliquer sur "Ajouter un livre"
2. Remplir:
   - ISBN: 978-2-1234-5680-3
   - Titre: Le Petit Prince
   - Editeur: Gallimard
   - Année: 1943
   - Exemplaires: 5
3. Soumettre et vérifier l'ajout

#### Badge de disponibilité
- Vérifier les badges:
  - Vert si exemplaires > 0
  - Rouge si exemplaires = 0

#### Modification
- L'ISBN devrait être désactivé (grisé) en mode édition

### 4. Test Emprunts

#### Création d'emprunt
1. Cliquer sur "Nouvel emprunt"
2. Sélectionner un étudiant
3. Sélectionner un livre disponible
4. Vérifier:
   - Le nombre d'exemplaires diminue de 1
   - L'emprunt apparaît dans la liste

#### Filtres
1. Cliquer sur "En cours"
   - Seuls les emprunts non retournés s'affichent
2. Cliquer sur "En retard"
   - Seuls les emprunts en retard s'affichent
3. Cliquer sur "Tous"
   - Tous les emprunts s'affichent

#### Retour de livre
1. Trouver un emprunt "En cours"
2. Cliquer sur "Retour"
3. Confirmer
4. Vérifier:
   - Badge devient "Retourné" (gris)
   - Date de retour apparaît
   - Amende affichée si en retard
   - Bouton "Retour" disparaît

### 5. Test Statistiques

#### Chargement
- Vérifier que toutes les données s'affichent:
  - 4 cards colorées avec nombres
  - Progress bar animée
  - Card résumé
  - Top 5 étudiants (si données)
  - Top 5 livres (si données)

#### Actualisation
1. Créer un emprunt
2. Aller sur Statistiques
3. Cliquer sur "Actualiser"
4. Vérifier la mise à jour des chiffres

### 6. Test des erreurs

#### Sans backend
1. Arrêter le backend
2. Recharger la page
3. Vérifier le message: "Impossible de se connecter au serveur"

#### Avec backend
1. Redémarrer le backend
2. Recharger la page
3. Vérifier que les données se chargent

### 7. Test responsive

#### Desktop (> 768px)
- Navbar complète sur une ligne
- Tables complètes visibles
- Cards sur 3-4 colonnes

#### Tablette (768px)
- Navbar avec bouton toggle
- Tables avec scroll horizontal
- Cards sur 2 colonnes

#### Mobile (< 576px)
- Menu hamburger
- Tables scrollables
- Cards empilées (1 colonne)

### 8. Test des animations

- Chaque changement de page devrait avoir l'animation fade-in
- Les alertes devraient apparaître en douceur
- Les modales devraient s'animer

## Tests automatisés (à implémenter)

### Tests unitaires
```bash
ng test
```

Composants à tester:
- ApiService (appels HTTP)
- EtudiantsComponent (CRUD)
- LivresComponent (CRUD)
- EmpruntsComponent (filtres + retour)
- StatsComponent (affichage)

### Tests E2E
```bash
ng e2e
```

Scénarios:
1. Parcours complet: ajout étudiant + livre + emprunt + retour
2. Validation des formulaires
3. Navigation entre pages
4. Gestion des erreurs

## Checklist de validation

- [ ] Toutes les routes fonctionnent
- [ ] CRUD étudiants complet
- [ ] CRUD livres complet
- [ ] Création et retour d'emprunts
- [ ] Filtres d'emprunts fonctionnels
- [ ] Statistiques à jour
- [ ] Modales s'ouvrent et se ferment
- [ ] Alertes s'affichent et se ferment
- [ ] Pas d'erreurs dans la console
- [ ] Design responsive
- [ ] Icônes affichées
- [ ] Navigation active visible
- [ ] Messages de confirmation
- [ ] Gestion des erreurs API

## Problèmes courants

### Modal ne se ferme pas
- Vérifier que Bootstrap JS est importé dans main.ts
- Vérifier l'attribut `data-bs-dismiss="modal"`

### Erreur CORS
- Le backend doit autoriser http://localhost:4200
- Vérifier la configuration CORS du backend

### Données ne se chargent pas
- Vérifier que le backend est sur le port 5001
- Vérifier l'URL dans api.service.ts
- Vérifier la console navigateur pour les erreurs

### Icônes manquantes
- Vérifier l'import dans styles.scss
- Vérifier que bootstrap-icons est installé

## Performance

### Temps de chargement attendus
- Première page: < 2s
- Navigation: instantanée
- Soumission formulaire: < 500ms
- Actualisation stats: < 300ms

### Optimisations possibles
- Lazy loading des modules
- Virtual scrolling pour grandes listes
- Cache des données (service avec BehaviorSubject)
- Pagination côté serveur
