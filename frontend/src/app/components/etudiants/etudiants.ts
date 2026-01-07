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

  etudiants: Etudiant[] = [];
  loading = false;
  error = '';
  modalError = '';
  successMessage = '';

  // Form data
  formData: Etudiant = { nom: '', prenom: '', email: '' };
  isEditing = false;
  editingId?: number;

  // Pending action
  private pendingAction: (() => void) | null = null;

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadEtudiants();
  }

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

  openAddModal(): void {
    this.formData = { nom: '', prenom: '', email: '' };
    this.isEditing = false;
    this.modalError = '';
  }

  openEditModal(etudiant: Etudiant): void {
    this.formData = { ...etudiant };
    this.isEditing = true;
    this.editingId = etudiant.id;
    this.modalError = '';
  }

  saveEtudiant(): void {
    if (!this.formData.nom || !this.formData.prenom || !this.formData.email) {
      this.modalError = 'Tous les champs sont requis';
      this.cdr.detectChanges();
      return;
    }

    this.loading = true;
    this.modalError = '';
    this.cdr.detectChanges();

    const operation = this.isEditing
      ? this.apiService.updateEtudiant(this.editingId!, this.formData)
      : this.apiService.addEtudiant(this.formData);

    operation.subscribe({
      next: () => {
        this.successMessage = this.isEditing
          ? 'Etudiant modifié avec succès'
          : 'Etudiant ajouté avec succès';
        this.loading = false;
        this.loadEtudiants();
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

  deleteEtudiant(id: number, nom: string, prenom: string): void {
    this.pendingAction = () => {
      this.loading = true;
      this.error = '';
      this.cdr.detectChanges();

      this.apiService.deleteEtudiant(id).subscribe({
        next: () => {
          this.successMessage = 'Etudiant supprimé avec succès';
          this.loading = false;
          this.loadEtudiants();
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
    this.confirmModal.show(`Voulez-vous vraiment supprimer l'étudiant ${prenom} ${nom} ?`);
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
    const modalElement = document.getElementById('etudiantModal');
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
