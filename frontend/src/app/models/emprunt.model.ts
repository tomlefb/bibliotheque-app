export interface Emprunt {
  id: number;
  etudiant_id: number;
  livre_id: string;
  nom: string;
  prenom: string;
  titre: string;
  date_emprunt: string;
  date_retour?: string;
  jours_retard?: number;
  amende?: number;
}
