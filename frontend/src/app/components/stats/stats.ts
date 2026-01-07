import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../services/api.service';
import { Stats as StatsModel, StatsOverview, TopEtudiant, TopLivre } from '../../models/stats.model';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-stats',
  imports: [CommonModule],
  templateUrl: './stats.html',
  styleUrl: './stats.scss',
})
export class Stats implements OnInit {
  stats?: StatsModel;
  loading = false;
  error = '';

  constructor(
    private apiService: ApiService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadStats();
  }

  loadStats(): void {
    this.loading = true;
    this.error = '';
    this.cdr.detectChanges();

    // Charger toutes les donnees en parallele avec forkJoin
    forkJoin({
      overview: this.apiService.getStats(),
      topEtudiants: this.apiService.getTopEtudiants(),
      topLivres: this.apiService.getTopLivres()
    }).subscribe({
      next: (data) => {
        const overview = data.overview as unknown as StatsOverview;

        // Construire l'objet stats complet
        this.stats = {
          total_etudiants: overview.totaux.etudiants,
          total_livres: overview.totaux.livres,
          total_exemplaires: overview.totaux.emprunts,
          emprunts_en_cours: overview.emprunts.en_cours,
          emprunts_en_retard: 0, // Sera calcule depuis les emprunts en retard
          livres_disponibles: overview.livres_disponibles,
          taux_emprunt: overview.taux_emprunt,
          top_etudiants: data.topEtudiants as TopEtudiant[],
          top_livres: data.topLivres as TopLivre[]
        };

        // Charger les emprunts en retard pour obtenir le nombre (uniquement non retournés)
        this.apiService.getEmpruntsEnRetard().subscribe({
          next: (empruntsRetard) => {
            if (this.stats) {
              this.stats.emprunts_en_retard = empruntsRetard.length;
              this.cdr.detectChanges();
            }
          },
          error: (err) => {
            console.error('Erreur chargement emprunts en retard:', err);
          }
        });

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

  dismissAlert(): void {
    this.error = '';
    this.cdr.detectChanges();
  }
}
