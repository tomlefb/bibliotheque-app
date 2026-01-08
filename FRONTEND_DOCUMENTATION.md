# Documentation Frontend - Angular

**Projet** : Application de Gestion de Bibliothèque
**Auteurs** : Tom LEFEVRE-BONZON & Ilies MAHOUDEAU
**Module** : Administration de Bases de Données - B3 Dev SDV

---

## 1. Vue d'ensemble

Le frontend est une **Single Page Application (SPA)** développée avec Angular 21. Elle communique avec le backend Flask via des appels HTTP REST.

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Angular)                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  Home   │  │Etudiants│  │ Livres  │  │Emprunts │    │
│  │ (Stats) │  │  CRUD   │  │  CRUD   │  │  CRUD   │    │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘    │
│       └────────────┴────────────┴────────────┘          │
│                         │                                │
│                   ApiService                             │
│                         │ HTTP/JSON                      │
└─────────────────────────┼───────────────────────────────┘
                          ▼
                   Backend Flask (:5001)
```

---

## 2. Technologies utilisées

| Technologie | Version | Rôle |
|-------------|---------|------|
| **Angular** | 21.x | Framework frontend |
| **TypeScript** | 5.x | Langage typé (superset de JS) |
| **Bootstrap** | 5.3 | Framework CSS |
| **Bootstrap Icons** | 1.x | Bibliothèque d'icônes |
| **RxJS** | 7.x | Programmation réactive (Observables) |

---

## 3. Structure du projet

```
frontend/src/app/
├── app.ts                      # Composant racine
├── app.routes.ts               # Configuration des routes
├── components/
│   ├── home/
│   │   ├── home.ts             # Page d'accueil (stats)
│   │   ├── home.html
│   │   └── home.scss
│   ├── etudiants/
│   │   ├── etudiants.ts        # Gestion étudiants
│   │   ├── etudiants.html
│   │   └── etudiants.scss
│   ├── livres/
│   │   ├── livres.ts           # Gestion livres
│   │   ├── livres.html
│   │   └── livres.scss
│   ├── emprunts/
│   │   ├── emprunts.ts         # Gestion emprunts
│   │   ├── emprunts.html
│   │   └── emprunts.scss
│   └── shared/
│       └── confirm-modal/      # Modal réutilisable
│           ├── confirm-modal.ts
│           └── confirm-modal.html
├── services/
│   └── api.service.ts          # Communication HTTP
└── models/
    ├── etudiant.model.ts       # Interface Etudiant
    ├── livre.model.ts          # Interface Livre
    ├── emprunt.model.ts        # Interface Emprunt
    └── stats.model.ts          # Interface Stats
```

---

## 4. Standalone Components

Angular 21 utilise les **standalone components** (plus besoin de NgModule) :

```typescript
@Component({
  selector: 'app-etudiants',
  standalone: true,                              // Composant autonome
  imports: [CommonModule, FormsModule, ConfirmModal],  // Imports directs
  templateUrl: './etudiants.html',
  styleUrl: './etudiants.scss',
})
export class Etudiants implements OnInit {
  // ...
}
```

**Avantages :**
- Pas de déclaration dans un module
- Imports explicites et clairs
- Meilleur tree-shaking (bundle plus petit)

---

## 5. Routing (Navigation)

### 5.1 Configuration des routes (app.routes.ts)

```typescript
import { Routes } from '@angular/router';
import { Home } from './components/home/home';
import { Etudiants } from './components/etudiants/etudiants';
import { Livres } from './components/livres/livres';
import { Emprunts } from './components/emprunts/emprunts';

export const routes: Routes = [
  { path: '', component: Home },
  { path: 'etudiants', component: Etudiants },
  { path: 'livres', component: Livres },
  { path: 'emprunts', component: Emprunts },
  { path: '**', redirectTo: '' }  // Fallback
];
```

### 5.2 Navigation dans le template

```html
<!-- Barre de navigation -->
<nav class="navbar navbar-expand-lg navbar-dark bg-primary">
  <div class="container">
    <a class="navbar-brand" routerLink="/">Bibliothèque</a>
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" routerLink="/etudiants" routerLinkActive="active">
          <i class="bi bi-people"></i> Étudiants
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" routerLink="/livres" routerLinkActive="active">
          <i class="bi bi-book"></i> Livres
        </a>
      </li>
      <li class="nav-item">
        <a class="nav-link" routerLink="/emprunts" routerLinkActive="active">
          <i class="bi bi-arrow-left-right"></i> Emprunts
        </a>
      </li>
    </ul>
  </div>
</nav>

<!-- Zone de contenu (change selon la route) -->
<router-outlet></router-outlet>
```

---

## 6. Modèles TypeScript

### 6.1 Interface Etudiant

```typescript
// models/etudiant.model.ts
export interface Etudiant {
  id?: number;           // Optionnel car généré par la BDD
  nom: string;
  prenom: string;
  email: string;
  created_at?: string;
}
```

### 6.2 Interface Livre

```typescript
// models/livre.model.ts
export interface Livre {
  isbn: string;
  titre: string;
  editeur: string;
  annee_publication: number;
  exemplaires_dispo: number;
  created_at?: string;
}
```

### 6.3 Interface Emprunt

```typescript
// models/emprunt.model.ts
export interface Emprunt {
  id: number;
  etudiant_id: number;
  livre_isbn: string;
  date_emprunt: string;
  date_retour: string | null;
  // Champs ajoutés par les JOINs
  nom?: string;
  prenom?: string;
  titre?: string;
  // Champs calculés
  jours_retard?: number;
  amende?: number;
}
```

---

## 7. Service API (api.service.ts)

### 7.1 Structure du service

```typescript
import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'  // Singleton disponible partout
})
export class ApiService {
  private readonly API_URL = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  // === ÉTUDIANTS ===
  getEtudiants(): Observable<Etudiant[]> {
    return this.http.get<Etudiant[]>(`${this.API_URL}/etudiants`)
      .pipe(catchError(this.handleError));
  }

  addEtudiant(etudiant: Etudiant): Observable<Etudiant> {
    return this.http.post<Etudiant>(`${this.API_URL}/etudiants`, etudiant)
      .pipe(catchError(this.handleError));
  }

  updateEtudiant(id: number, etudiant: Etudiant): Observable<Etudiant> {
    return this.http.put<Etudiant>(`${this.API_URL}/etudiants/${id}`, etudiant)
      .pipe(catchError(this.handleError));
  }

  deleteEtudiant(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/etudiants/${id}`)
      .pipe(catchError(this.handleError));
  }

  // ... idem pour Livres et Emprunts
}
```

### 7.2 Gestion des erreurs

```typescript
private handleError = (error: HttpErrorResponse) => {
  let errorMessage = 'Une erreur est survenue';

  if (error.error instanceof ErrorEvent) {
    // Erreur côté client
    errorMessage = `Erreur: ${error.error.message}`;
  } else {
    // Erreur côté serveur
    if (error.status === 0) {
      errorMessage = 'Impossible de se connecter au serveur.';
    } else if (error.error?.error) {
      // Traduire les erreurs PostgreSQL
      errorMessage = this.translateDatabaseError(error.error.error);
    } else {
      errorMessage = `Erreur ${error.status}: ${error.message}`;
    }
  }

  return throwError(() => new Error(errorMessage));
}

private translateDatabaseError(message: string): string {
  // Email déjà utilisé
  if (message.includes('etudiant_email_key') || message.includes('duplicate')) {
    return 'Cette adresse email est déjà utilisée par un autre étudiant.';
  }
  // ISBN déjà existant
  if (message.includes('livre_pkey')) {
    return 'Ce numéro ISBN existe déjà dans la base de données.';
  }
  // Clé étrangère (emprunts liés)
  if (message.includes('foreign key')) {
    return 'Impossible de supprimer : des emprunts sont associés à cet élément.';
  }
  return message;
}
```

---

## 8. Composant Étudiants (exemple complet)

### 8.1 TypeScript (etudiants.ts)

```typescript
import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Etudiant } from '../../models/etudiant.model';
import { ConfirmModal } from '../shared/confirm-modal/confirm-modal';

declare const bootstrap: any;

@Component({
  selector: 'app-etudiants',
  imports: [CommonModule, FormsModule, ConfirmModal],
  templateUrl: './etudiants.html',
  styleUrl: './etudiants.scss',
})
export class Etudiants implements OnInit {
  @ViewChild(ConfirmModal) confirmModal!: ConfirmModal;

  // État du composant
  etudiants: Etudiant[] = [];
  loading = false;
  error = '';
  modalError = '';
  successMessage = '';

  // Formulaire
  formData: Etudiant = { nom: '', prenom: '', email: '' };
  isEditing = false;
  editingId?: number;

  // Action en attente de confirmation
  private pendingAction: (() => void) | null = null;

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadEtudiants();
  }

  // === CHARGEMENT ===
  loadEtudiants(): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();

    this.apiService.getEtudiants().subscribe({
      next: (data) => {
        this.etudiants = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        this.error = err.message;
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  // === MODALS ===
  openAddModal(): void {
    this.formData = { nom: '', prenom: '', email: '' };
    this.isEditing = false;
    this.modalError = '';
  }

  openEditModal(etudiant: Etudiant): void {
    this.formData = { ...etudiant };  // Copie pour ne pas modifier l'original
    this.isEditing = true;
    this.editingId = etudiant.id;
    this.modalError = '';
  }

  // === SAUVEGARDE ===
  saveEtudiant(): void {
    // Validation
    if (!this.formData.nom || !this.formData.prenom || !this.formData.email) {
      this.modalError = 'Tous les champs sont requis';
      return;
    }

    this.loading = true;
    this.modalError = '';

    const operation = this.isEditing
      ? this.apiService.updateEtudiant(this.editingId!, this.formData)
      : this.apiService.addEtudiant(this.formData);

    operation.subscribe({
      next: () => {
        this.successMessage = this.isEditing
          ? 'Étudiant modifié avec succès'
          : 'Étudiant ajouté avec succès';
        this.loading = false;
        this.loadEtudiants();
        this.closeModal();
        // Auto-dismiss après 3 secondes
        setTimeout(() => {
          this.successMessage = '';
          this.cdr.detectChanges();
        }, 3000);
      },
      error: (err) => {
        this.modalError = err.message;
        this.loading = false;
      }
    });
  }

  // === SUPPRESSION ===
  deleteEtudiant(id: number, nom: string, prenom: string): void {
    // Stocker l'action pour exécution après confirmation
    this.pendingAction = () => {
      this.loading = true;
      this.apiService.deleteEtudiant(id).subscribe({
        next: () => {
          this.successMessage = 'Étudiant supprimé avec succès';
          this.loading = false;
          this.loadEtudiants();
          setTimeout(() => {
            this.successMessage = '';
            this.cdr.detectChanges();
          }, 3000);
        },
        error: (err) => {
          this.error = err.message;
          this.loading = false;
          setTimeout(() => {
            this.error = '';
            this.cdr.detectChanges();
          }, 5000);
        }
      });
    };
    // Afficher le modal de confirmation
    this.confirmModal.show(`Supprimer l'étudiant ${prenom} ${nom} ?`);
  }

  onConfirmAction(): void {
    if (this.pendingAction) {
      this.pendingAction();
      this.pendingAction = null;
    }
  }

  // === UTILITAIRES ===
  closeModal(): void {
    const modalElement = document.getElementById('etudiantModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
      const modal = bootstrap.Modal.getInstance(modalElement)
                 || new bootstrap.Modal(modalElement);
      modal.hide();
    }
  }

  dismissAlert(): void {
    this.error = '';
    this.modalError = '';
    this.successMessage = '';
  }
}
```

### 8.2 Template HTML (etudiants.html)

```html
<div class="container mt-4 fade-in">
  <!-- En-tête -->
  <div class="d-flex justify-content-between align-items-center mb-4">
    <h2><i class="bi bi-people me-2"></i>Gestion des Étudiants</h2>
    <button class="btn btn-primary" data-bs-toggle="modal"
            data-bs-target="#etudiantModal" (click)="openAddModal()">
      <i class="bi bi-plus-circle me-1"></i>Ajouter un étudiant
    </button>
  </div>

  <!-- Alertes -->
  <div *ngIf="error" class="alert alert-danger alert-dismissible fade show">
    <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
    <button type="button" class="btn-close" (click)="dismissAlert()"></button>
  </div>

  <div *ngIf="successMessage" class="alert alert-success alert-dismissible fade show">
    <i class="bi bi-check-circle me-2"></i>{{ successMessage }}
    <button type="button" class="btn-close" (click)="dismissAlert()"></button>
  </div>

  <!-- Loader -->
  <div *ngIf="loading" class="text-center my-5">
    <div class="spinner-border text-primary"></div>
  </div>

  <!-- Message si vide -->
  <div *ngIf="!loading && etudiants.length === 0" class="alert alert-info">
    <i class="bi bi-info-circle me-2"></i>Aucun étudiant trouvé.
  </div>

  <!-- Tableau -->
  <div *ngIf="!loading && etudiants.length > 0" class="table-responsive">
    <table class="table table-hover table-striped">
      <thead class="table-dark">
        <tr>
          <th>ID</th>
          <th>Nom</th>
          <th>Prénom</th>
          <th>Email</th>
          <th class="text-end">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let etudiant of etudiants">
          <td>{{ etudiant.id }}</td>
          <td>{{ etudiant.nom }}</td>
          <td>{{ etudiant.prenom }}</td>
          <td>{{ etudiant.email }}</td>
          <td class="text-end">
            <button class="btn btn-sm btn-outline-primary me-2"
                    data-bs-toggle="modal" data-bs-target="#etudiantModal"
                    (click)="openEditModal(etudiant)">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger"
                    (click)="deleteEtudiant(etudiant.id!, etudiant.nom, etudiant.prenom)">
              <i class="bi bi-trash"></i>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</div>

<!-- Modal d'ajout/modification -->
<div class="modal fade" id="etudiantModal" tabindex="-1">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">
          {{ isEditing ? 'Modifier' : 'Ajouter' }} un étudiant
        </h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <!-- Erreur dans le modal -->
        <div *ngIf="modalError" class="alert alert-danger">
          <i class="bi bi-exclamation-triangle me-2"></i>{{ modalError }}
        </div>

        <form>
          <div class="mb-3">
            <label for="nom" class="form-label">Nom</label>
            <input type="text" class="form-control" id="nom"
                   [(ngModel)]="formData.nom" name="nom" required>
          </div>
          <div class="mb-3">
            <label for="prenom" class="form-label">Prénom</label>
            <input type="text" class="form-control" id="prenom"
                   [(ngModel)]="formData.prenom" name="prenom" required>
          </div>
          <div class="mb-3">
            <label for="email" class="form-label">Email</label>
            <input type="email" class="form-control" id="email"
                   [(ngModel)]="formData.email" name="email" required>
          </div>
        </form>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
          Annuler
        </button>
        <button type="button" class="btn btn-primary" (click)="saveEtudiant()"
                [disabled]="loading">
          <span *ngIf="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ isEditing ? 'Modifier' : 'Ajouter' }}
        </button>
      </div>
    </div>
  </div>
</div>

<!-- Modal de confirmation (composant réutilisable) -->
<app-confirm-modal (confirmed)="onConfirmAction()"></app-confirm-modal>
```

---

## 9. Two-Way Data Binding

Angular utilise le **two-way binding** avec `[(ngModel)]` :

```html
<input [(ngModel)]="formData.nom" name="nom">
```

Équivalent à :
```html
<input [ngModel]="formData.nom" (ngModelChange)="formData.nom = $event">
```

**Fonctionnement :**
1. `[ngModel]` : affiche la valeur de `formData.nom` dans l'input
2. `(ngModelChange)` : met à jour `formData.nom` quand l'utilisateur tape

---

## 10. Observables et RxJS

### 10.1 Qu'est-ce qu'un Observable ?

Un **Observable** est un flux de données asynchrone. On s'y "abonne" avec `.subscribe()` :

```typescript
this.apiService.getEtudiants().subscribe({
  next: (data) => {
    // Succès : data contient le tableau d'étudiants
    this.etudiants = data;
  },
  error: (err) => {
    // Erreur : err contient le message d'erreur
    this.error = err.message;
  }
});
```

### 10.2 Opérateurs RxJS

```typescript
import { catchError } from 'rxjs/operators';

getEtudiants(): Observable<Etudiant[]> {
  return this.http.get<Etudiant[]>(`${this.API_URL}/etudiants`)
    .pipe(
      catchError(this.handleError)  // Intercepte les erreurs
    );
}
```

---

## 11. Directives Angular

### 11.1 *ngIf - Affichage conditionnel

```html
<!-- Affiche seulement si loading est true -->
<div *ngIf="loading">Chargement...</div>

<!-- Affiche seulement si pas de loading ET tableau non vide -->
<div *ngIf="!loading && etudiants.length > 0">
  <!-- Tableau ici -->
</div>
```

### 11.2 *ngFor - Boucle

```html
<tr *ngFor="let etudiant of etudiants">
  <td>{{ etudiant.nom }}</td>
  <td>{{ etudiant.prenom }}</td>
</tr>
```

### 11.3 [ngClass] - Classes dynamiques

```html
<!-- Ajoute 'bg-success' si dispo > 0, sinon 'bg-danger' -->
<span [ngClass]="livre.exemplaires_dispo > 0 ? 'bg-success' : 'bg-danger'">
  {{ livre.exemplaires_dispo }}
</span>
```

### 11.4 Pipes - Formatage

```html
<!-- Formate la date en dd/MM/yyyy -->
<td>{{ emprunt.date_emprunt | date:'dd/MM/yyyy' }}</td>

<!-- Condition ternaire avec pipe -->
<td>{{ emprunt.date_retour ? (emprunt.date_retour | date:'dd/MM/yyyy') : '-' }}</td>
```

---

## 12. Modal de confirmation réutilisable

### 12.1 Composant (confirm-modal.ts)

```typescript
import { Component, Output, EventEmitter, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

declare const bootstrap: any;

@Component({
  selector: 'app-confirm-modal',
  imports: [CommonModule],
  templateUrl: './confirm-modal.html',
})
export class ConfirmModal implements AfterViewInit {
  @Output() confirmed = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  message = '';
  private modalInstance: any;
  private modalElement: any;

  ngAfterViewInit(): void {
    this.modalElement = document.getElementById('confirmModal');
  }

  show(message: string): void {
    this.message = message;
    if (this.modalElement && typeof bootstrap !== 'undefined') {
      this.modalInstance = new bootstrap.Modal(this.modalElement);
      this.modalInstance.show();
    }
  }

  onConfirm(): void {
    this.confirmed.emit();  // Émet l'événement vers le parent
    this.modalInstance?.hide();
  }

  onCancel(): void {
    this.cancelled.emit();
    this.modalInstance?.hide();
  }
}
```

### 12.2 Utilisation dans un parent

```html
<!-- Dans etudiants.html -->
<app-confirm-modal (confirmed)="onConfirmAction()"></app-confirm-modal>
```

```typescript
// Dans etudiants.ts
deleteEtudiant(id: number): void {
  this.pendingAction = () => {
    // Suppression effective ici
  };
  this.confirmModal.show('Voulez-vous vraiment supprimer ?');
}

onConfirmAction(): void {
  if (this.pendingAction) {
    this.pendingAction();
    this.pendingAction = null;
  }
}
```

---

## 13. Page d'accueil (Statistiques)

### 13.1 Appel API

```typescript
loadStats(): void {
  this.apiService.getStats().subscribe({
    next: (data) => {
      this.stats = data;
      // data contient : totaux, emprunts, livres_disponibles, taux_emprunt
    }
  });

  this.apiService.getTopEtudiants().subscribe({
    next: (data) => this.topEtudiants = data
  });

  this.apiService.getTopLivres().subscribe({
    next: (data) => this.topLivres = data
  });
}
```

### 13.2 Affichage des stats

```html
<div class="row">
  <div class="col-md-3">
    <div class="stat-card">
      <i class="bi bi-people stat-icon text-primary"></i>
      <div class="stat-value">{{ stats?.totaux?.etudiants || 0 }}</div>
      <div class="stat-label">Étudiants</div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="stat-card">
      <i class="bi bi-book stat-icon text-success"></i>
      <div class="stat-value">{{ stats?.totaux?.livres || 0 }}</div>
      <div class="stat-label">Livres</div>
    </div>
  </div>
  <!-- ... -->
</div>
```

---

## 14. Gestion des emprunts (filtres)

### 14.1 Filtrage côté frontend

```typescript
currentFilter = 'tous';
searchTerm = '';
filteredEmprunts: Emprunt[] = [];

filterEmprunts(filtre: string): void {
  this.currentFilter = filtre;
  this.loadEmprunts();  // Recharge depuis l'API
}

// L'API a des endpoints spécifiques :
// GET /api/emprunts           → Tous
// GET /api/emprunts/en-cours  → Non retournés
// GET /api/emprunts/en-retard → En retard (> 14 jours)
```

### 14.2 Recherche locale

```typescript
applySearch(): void {
  if (!this.searchTerm.trim()) {
    this.filteredEmprunts = this.emprunts;
  } else {
    const term = this.searchTerm.toLowerCase();
    this.filteredEmprunts = this.emprunts.filter(e =>
      e.nom.toLowerCase().includes(term) ||
      e.prenom.toLowerCase().includes(term) ||
      e.titre.toLowerCase().includes(term)
    );
  }
}
```

---

## 15. Lancer le frontend

### 15.1 Installation

```bash
cd frontend
npm install
```

### 15.2 Développement

```bash
npm start
# ou
ng serve

# → http://localhost:4200
```

### 15.3 Build production

```bash
ng build --configuration production
# → Fichiers dans dist/frontend/
```

---

## 16. Résumé des concepts Angular

| Concept | Utilisation |
|---------|-------------|
| **Standalone Components** | Composants autonomes sans NgModule |
| **Routing** | Navigation entre pages |
| **Services** | ApiService pour les appels HTTP |
| **Dependency Injection** | Injection du service dans les composants |
| **Two-Way Binding** | `[(ngModel)]` pour les formulaires |
| **Observables (RxJS)** | Gestion des appels asynchrones |
| **Directives** | `*ngIf`, `*ngFor`, `[ngClass]` |
| **Pipes** | `date` pour formater les dates |
| **@Output / EventEmitter** | Communication enfant → parent |
| **@ViewChild** | Accès à un composant enfant |
| **ChangeDetectorRef** | Forcer la mise à jour de la vue |

---

**Document préparé pour l'oral - Frontend Angular**
**Tom LEFEVRE-BONZON & Ilies MAHOUDEAU - B3 Dev SDV**
