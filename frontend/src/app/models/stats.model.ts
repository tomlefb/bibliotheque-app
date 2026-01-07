// Interface pour la reponse de /api/stats/overview
export interface StatsOverview {
  totaux: {
    etudiants: number;
    livres: number;
    emprunts: number;
  };
  emprunts: {
    en_cours: number;
    termines: number;
  };
  livres_disponibles: number;
  taux_emprunt: number;
}

// Interface pour les top etudiants
export interface TopEtudiant {
  nom: string;
  prenom: string;
  nombre_emprunts: number;
}

// Interface pour les top livres
export interface TopLivre {
  titre: string;
  nombre_emprunts: number;
}

// Interface pour les emprunts en retard
export interface EmpruntRetard {
  id: number;
  etudiant_nom: string;
  etudiant_prenom: string;
  livre_titre: string;
  date_emprunt: string;
  date_retour_prevue: string;
  jours_retard: number;
}

// Interface combinee pour l'affichage
export interface Stats {
  total_etudiants: number;
  total_livres: number;
  total_exemplaires: number;
  emprunts_en_cours: number;
  emprunts_en_retard: number;
  livres_disponibles: number;
  taux_emprunt: number;
  top_etudiants: TopEtudiant[];
  top_livres: TopLivre[];
}
