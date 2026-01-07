import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Etudiant } from '../models/etudiant.model';
import { Livre } from '../models/livre.model';
import { Emprunt } from '../models/emprunt.model';
import { Stats } from '../models/stats.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private readonly API_URL = 'http://localhost:5001/api';

  constructor(private http: HttpClient) {}

  // Etudiants
  getEtudiants(): Observable<Etudiant[]> {
    return this.http.get<Etudiant[]>(`${this.API_URL}/etudiants`)
      .pipe(catchError(this.handleError));
  }

  getEtudiant(id: number): Observable<Etudiant> {
    return this.http.get<Etudiant>(`${this.API_URL}/etudiants/${id}`)
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

  // Livres
  getLivres(): Observable<Livre[]> {
    return this.http.get<Livre[]>(`${this.API_URL}/livres`)
      .pipe(catchError(this.handleError));
  }

  getLivre(isbn: string): Observable<Livre> {
    return this.http.get<Livre>(`${this.API_URL}/livres/${isbn}`)
      .pipe(catchError(this.handleError));
  }

  addLivre(livre: Livre): Observable<Livre> {
    return this.http.post<Livre>(`${this.API_URL}/livres`, livre)
      .pipe(catchError(this.handleError));
  }

  updateLivre(isbn: string, livre: Livre): Observable<Livre> {
    return this.http.put<Livre>(`${this.API_URL}/livres/${isbn}`, livre)
      .pipe(catchError(this.handleError));
  }

  deleteLivre(isbn: string): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/livres/${isbn}`)
      .pipe(catchError(this.handleError));
  }

  // Emprunts
  getEmprunts(): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(`${this.API_URL}/emprunts`)
      .pipe(catchError(this.handleError));
  }

  getEmpruntsEnCours(): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(`${this.API_URL}/emprunts/en-cours`)
      .pipe(catchError(this.handleError));
  }

  getEmpruntsEnRetard(): Observable<Emprunt[]> {
    return this.http.get<Emprunt[]>(`${this.API_URL}/emprunts/en-retard`)
      .pipe(catchError(this.handleError));
  }

  addEmprunt(emprunt: { etudiant_id: number, livre_id: string }): Observable<Emprunt> {
    return this.http.post<Emprunt>(`${this.API_URL}/emprunts`, emprunt)
      .pipe(catchError(this.handleError));
  }

  retourEmprunt(id: number): Observable<void> {
    return this.http.post<void>(`${this.API_URL}/emprunts/${id}/retourner`, {})
      .pipe(catchError(this.handleError));
  }

  deleteEmprunt(id: number): Observable<void> {
    return this.http.delete<void>(`${this.API_URL}/emprunts/${id}`)
      .pipe(catchError(this.handleError));
  }

  // Stats
  getStats(): Observable<Stats> {
    return this.http.get<Stats>(`${this.API_URL}/stats/overview`)
      .pipe(catchError(this.handleError));
  }

  getTopEtudiants(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/stats/top-etudiants`)
      .pipe(catchError(this.handleError));
  }

  getTopLivres(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_URL}/stats/top-livres`)
      .pipe(catchError(this.handleError));
  }

  private handleError = (error: HttpErrorResponse) => {
    let errorMessage = 'Une erreur est survenue';

    if (error.error instanceof ErrorEvent) {
      errorMessage = `Erreur: ${error.error.message}`;
    } else {
      if (error.status === 0) {
        errorMessage = 'Impossible de se connecter au serveur. Vérifiez que le backend est démarré.';
      } else if (error.error?.error) {
        // Transformer les erreurs de contraintes DB en messages clairs
        errorMessage = this.translateDatabaseError(error.error.error);
      } else {
        errorMessage = `Erreur ${error.status}: ${error.message}`;
      }
    }

    return throwError(() => new Error(errorMessage));
  }

  private translateDatabaseError(message: string): string {
    // Contrainte d'unicité sur l'email
    if (message.includes('etudiant_email_key') || (message.includes('duplicate') && message.includes('email'))) {
      return 'Cette adresse email est déjà utilisée par un autre étudiant.';
    }
    // Contrainte d'unicité sur l'ISBN
    if (message.includes('livre_pkey') || (message.includes('duplicate') && message.includes('isbn'))) {
      return 'Ce numéro ISBN existe déjà dans la base de données.';
    }
    // Contrainte de clé étrangère
    if (message.includes('foreign key') || message.includes('violates foreign key')) {
      if (message.includes('emprunt')) {
        return 'Impossible de supprimer : des emprunts sont associés à cet élément.';
      }
      return 'Opération impossible : des données liées existent.';
    }
    // Message par défaut
    return message;
  }
}
