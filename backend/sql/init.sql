-- Script de création des tables pour la bibliothèque universitaire
-- Base de données: bibliotheque

-- Création de la base (si elle n'existe pas)
-- Décommenter si vous devez créer la base:
-- CREATE DATABASE bibliotheque;

-- Se connecter à la base bibliotheque avant d'exécuter ce qui suit

-- Suppression des tables existantes (dans l'ordre des dépendances)
DROP TABLE IF EXISTS emprunt CASCADE;
DROP TABLE IF EXISTS livre CASCADE;
DROP TABLE IF EXISTS etudiant CASCADE;

-- Table etudiant
CREATE TABLE etudiant (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table livre
CREATE TABLE livre (
    id SERIAL PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    auteur VARCHAR(200) NOT NULL,
    annee_publication INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (annee_publication IS NULL OR (annee_publication >= 1000 AND annee_publication <= EXTRACT(YEAR FROM CURRENT_DATE)))
);

-- Table emprunt
CREATE TABLE emprunt (
    id SERIAL PRIMARY KEY,
    etudiant_id INTEGER NOT NULL REFERENCES etudiant(id) ON DELETE RESTRICT,
    livre_id INTEGER NOT NULL REFERENCES livre(id) ON DELETE RESTRICT,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (date_retour IS NULL OR date_retour >= date_emprunt)
);

-- Index pour améliorer les performances des recherches
CREATE INDEX idx_etudiant_nom ON etudiant(nom);
CREATE INDEX idx_etudiant_email ON etudiant(email);
CREATE INDEX idx_livre_titre ON livre(titre);
CREATE INDEX idx_livre_auteur ON livre(auteur);
CREATE INDEX idx_emprunt_etudiant ON emprunt(etudiant_id);
CREATE INDEX idx_emprunt_livre ON emprunt(livre_id);
CREATE INDEX idx_emprunt_date_retour ON emprunt(date_retour);

-- Commentaires sur les tables
COMMENT ON TABLE etudiant IS 'Table des étudiants inscrits à la bibliothèque';
COMMENT ON TABLE livre IS 'Catalogue des livres disponibles';
COMMENT ON TABLE emprunt IS 'Historique des emprunts de livres';

-- Commentaires sur les colonnes importantes
COMMENT ON COLUMN emprunt.date_retour IS 'NULL si le livre n''est pas encore retourné';

-- Afficher un message de confirmation
SELECT 'Tables créées avec succès!' AS message;
