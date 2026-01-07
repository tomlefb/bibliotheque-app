import { Component, OnInit, ChangeDetectorRef, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../services/api.service';
import { Livre } from '../../models/livre.model';
import { ConfirmModal } from '../shared/confirm-modal/confirm-modal';

declare const bootstrap: any;

@Component({
  selector: 'app-livres',
  imports: [CommonModule, FormsModule, ConfirmModal],
  templateUrl: './livres.html',
  styleUrl: './livres.scss',
})
export class Livres implements OnInit {
  @ViewChild(ConfirmModal) confirmModal!: ConfirmModal;

  livres: Livre[] = [];
  loading = false;
  error = '';
  modalError = '';
  successMessage = '';

  // Form data
  formData: Livre = { isbn: '', titre: '', editeur: '', annee_publication: new Date().getFullYear(), exemplaires_dispo: 1 };
  isEditing = false;
  editingIsbn?: string;

  // Pending action
  private pendingAction: (() => void) | null = null;

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadLivres();
  }

  loadLivres(): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();

    this.apiService.getLivres().subscribe({
      next: (data) => {
        this.livres = data;
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

  openAddModal(): void {
    this.formData = { isbn: '', titre: '', editeur: '', annee_publication: new Date().getFullYear(), exemplaires_dispo: 1 };
    this.isEditing = false;
    this.modalError = '';
  }

  openEditModal(livre: Livre): void {
    this.formData = { ...livre };
    this.isEditing = true;
    this.editingIsbn = livre.isbn;
    this.modalError = '';
  }

  saveLivre(): void {
    if (!this.formData.isbn || !this.formData.titre || !this.formData.editeur) {
      this.modalError = 'ISBN, titre et éditeur sont requis';
      this.cdr.detectChanges();
      return;
    }

    if (this.formData.annee_publication < 1000 || this.formData.annee_publication > new Date().getFullYear() + 1) {
      this.modalError = 'Année de publication invalide';
      this.cdr.detectChanges();
      return;
    }

    if (this.formData.exemplaires_dispo < 0) {
      this.modalError = 'Le nombre d\'exemplaires ne peut pas être négatif';
      this.cdr.detectChanges();
      return;
    }

    this.loading = true;
    this.modalError = '';
    this.cdr.detectChanges();

    const operation = this.isEditing
      ? this.apiService.updateLivre(this.editingIsbn!, this.formData)
      : this.apiService.addLivre(this.formData);

    operation.subscribe({
      next: () => {
        this.successMessage = this.isEditing
          ? 'Livre modifié avec succès'
          : 'Livre ajouté avec succès';
        this.loading = false;
        this.loadLivres();
        this.closeModal();
        this.cdr.detectChanges();
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

  deleteLivre(isbn: string, titre: string): void {
    this.pendingAction = () => {
      this.loading = true;
      this.error = '';
      this.cdr.detectChanges();

      this.apiService.deleteLivre(isbn).subscribe({
        next: () => {
          this.successMessage = 'Livre supprimé avec succès';
          this.loading = false;
          this.loadLivres();
          this.cdr.detectChanges();
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
    this.confirmModal.show(`Voulez-vous vraiment supprimer le livre "${titre}" ?`);
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
    const modalElement = document.getElementById('livreModal');
    if (modalElement && typeof bootstrap !== 'undefined') {
      const modal = bootstrap.Modal.getInstance(modalElement) || new bootstrap.Modal(modalElement);
      modal.hide();
    }
  }

  dismissAlert(): void {
    this.error = '';
    this.successMessage = '';
    this.cdr.detectChanges();
  }
}
