import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Emprunt } from '../../models/emprunt.model';
import { Etudiant } from '../../models/etudiant.model';
import { Livre } from '../../models/livre.model';
import { ConfirmModal } from '../shared/confirm-modal/confirm-modal';

declare const bootstrap: any;

@Component({
  selector: 'app-emprunts',
  imports: [CommonModule, FormsModule, ConfirmModal],
  templateUrl: './emprunts.html',
  styleUrl: './emprunts.scss',
})
export class Emprunts implements OnInit {
  @ViewChild(ConfirmModal) confirmModal!: ConfirmModal;

  emprunts: Emprunt[] = [];
  filteredEmprunts: Emprunt[] = [];
  etudiants: Etudiant[] = [];
  livres: Livre[] = [];
  loading = false;
  error = '';
  modalError = '';
  successMessage = '';
  activeFilter = 'tous';
  searchTerm = '';

  // Form data
  formData = { etudiant_id: 0, livre_id: '' };

  // Pending action
  private pendingAction: (() => void) | null = null;

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadEmprunts();
    this.loadEtudiants();
    this.loadLivres();
  }

  loadEmprunts(): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();

    let request;
    switch (this.activeFilter) {
      case 'en_cours':
        request = this.apiService.getEmpruntsEnCours();
        break;
      case 'en_retard':
        request = this.apiService.getEmpruntsEnRetard();
        break;
      default:
        request = this.apiService.getEmprunts();
    }

    request.subscribe({
      next: (data) => {
        this.emprunts = data;
        this.applySearch();
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

  loadEtudiants(): void {
    this.apiService.getEtudiants().subscribe({
      next: (data) => {
        this.etudiants = data;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erreur lors du chargement des étudiants:', err);
      }
    });
  }

  loadLivres(): void {
    this.apiService.getLivres().subscribe({
      next: (data) => {
        this.livres = data.filter(l => l.exemplaires_dispo > 0);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Erreur lors du chargement des livres:', err);
      }
    });
  }

  filterEmprunts(filtre: string): void {
    this.activeFilter = filtre;
    this.loadEmprunts();
  }

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
    this.cdr.detectChanges();
  }

  onSearchChange(): void {
    this.applySearch();
  }

  openAddModal(): void {
    this.formData = { etudiant_id: 0, livre_id: '' };
    this.modalError = '';
    this.loadLivres(); // Refresh available books
  }

  addEmprunt(): void {
    if (!this.formData.etudiant_id || !this.formData.livre_id) {
      this.modalError = 'Veuillez sélectionner un étudiant et un livre disponible';
      this.cdr.detectChanges();
      return;
    }

    this.loading = true;
    this.modalError = '';
    this.cdr.detectChanges();

    this.apiService.addEmprunt(this.formData).subscribe({
      next: () => {
        this.successMessage = 'Emprunt enregistré avec succès';
        this.loading = false;
        this.cdr.detectChanges();
        this.loadEmprunts();
        this.loadLivres();
        this.closeModal();
        // Auto-dismiss success message after 3 seconds
        setTimeout(() => {
          this.successMessage = '';
          this.cdr.detectChanges();
        }, 3000);
      },
      error: (err) => {
        this.modalError = err.message;
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }

  retourLivre(id: number, titre: string): void {
    this.pendingAction = () => {
      this.loading = true;
      this.error = '';
      this.cdr.detectChanges();

      this.apiService.retourEmprunt(id).subscribe({
        next: () => {
          this.successMessage = 'Retour enregistré avec succès';
          this.loading = false;
          this.cdr.detectChanges();
          this.loadEmprunts();
          this.loadLivres();
          // Auto-dismiss success message after 3 seconds
          setTimeout(() => {
            this.successMessage = '';
            this.cdr.detectChanges();
          }, 3000);
        },
        error: (err) => {
          this.error = err.message;
          this.loading = false;
          this.cdr.detectChanges();
          // Auto-dismiss error message after 5 seconds
          setTimeout(() => {
            this.error = '';
            this.cdr.detectChanges();
          }, 5000);
        }
      });
    };
    this.confirmModal.show(`Confirmer le retour du livre "${titre}" ?`);
  }

  deleteEmprunt(id: number, titre: string): void {
    this.pendingAction = () => {
      this.loading = true;
      this.error = '';
      this.cdr.detectChanges();

      this.apiService.deleteEmprunt(id).subscribe({
        next: () => {
          this.successMessage = 'Emprunt supprimé avec succès';
          this.loading = false;
          this.cdr.detectChanges();
          this.loadEmprunts();
          this.loadLivres();
          // Auto-dismiss success message after 3 seconds
          setTimeout(() => {
            this.successMessage = '';
            this.cdr.detectChanges();
          }, 3000);
        },
        error: (err) => {
          this.error = err.message;
          this.loading = false;
          this.cdr.detectChanges();
          // Auto-dismiss error message after 5 seconds
          setTimeout(() => {
            this.error = '';
            this.cdr.detectChanges();
          }, 5000);
        }
      });
    };
    this.confirmModal.show(`Voulez-vous vraiment supprimer l'emprunt du livre "${titre}" ?`);
  }

  onConfirmAction(): void {
    if (this.pendingAction) {
      this.pendingAction();
      this.pendingAction = null;
    }
  }

  onCancelAction(): void {
    this.pendingAction = null;
  }

  closeModal(): void {
    window.location.reload();
  }

  dismissAlert(): void {
    this.error = '';
    this.modalError = '';
    this.successMessage = '';
    this.cdr.detectChanges();
  }

  getStatusBadgeClass(emprunt: Emprunt): string {
    if (emprunt.date_retour) {
      return 'bg-secondary';
    }
    if (emprunt.jours_retard && emprunt.jours_retard > 0) {
      return 'bg-danger';
    }
    return 'bg-success';
  }

  getStatusText(emprunt: Emprunt): string {
    if (emprunt.date_retour) {
      return 'Retourné';
    }
    if (emprunt.jours_retard && emprunt.jours_retard > 0) {
      return `En retard (${emprunt.jours_retard}j)`;
    }
    return 'En cours';
  }
}
