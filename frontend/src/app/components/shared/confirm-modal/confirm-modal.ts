import { Component, EventEmitter, Output, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';

declare const bootstrap: any;

@Component({
  selector: 'app-confirm-modal',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="modal fade" id="confirmModal" tabindex="-1" aria-labelledby="confirmModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header bg-warning text-dark">
            <h5 class="modal-title" id="confirmModalLabel">
              <i class="bi bi-exclamation-triangle-fill me-2"></i>Confirmation
            </h5>
            <button type="button" class="btn-close" (click)="onCancel()" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p class="mb-0">{{ message }}</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" (click)="onCancel()">
              Annuler
            </button>
            <button type="button" class="btn btn-primary" (click)="onConfirm()">
              OK
            </button>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: []
})
export class ConfirmModal implements AfterViewInit {
  message = '';
  private modalInstance: any;
  private modalElement: any;

  @Output() confirmed = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  ngAfterViewInit(): void {
    // Get the modal element reference
    this.modalElement = document.getElementById('confirmModal');

    // Wait a bit for Bootstrap to be loaded
    setTimeout(() => {
      if (this.modalElement && typeof bootstrap !== 'undefined') {
        this.modalInstance = new bootstrap.Modal(this.modalElement, {
          backdrop: 'static',
          keyboard: false
        });
      }
    }, 500);
  }

  show(message: string): void {
    this.message = message;

    // Force change detection to update the message in the template
    setTimeout(() => {
      if (this.modalInstance) {
        this.modalInstance.show();
      } else if (this.modalElement && typeof bootstrap !== 'undefined') {
        // If instance doesn't exist yet, create it now
        this.modalInstance = new bootstrap.Modal(this.modalElement, {
          backdrop: 'static',
          keyboard: false
        });
        this.modalInstance.show();
      } else {
        console.error('Bootstrap Modal not available');
      }
    }, 0);
  }

  onConfirm(): void {
    this.confirmed.emit();
    if (this.modalInstance) {
      this.modalInstance.hide();
    }
  }

  onCancel(): void {
    this.cancelled.emit();
    if (this.modalInstance) {
      this.modalInstance.hide();
    }
  }
}
