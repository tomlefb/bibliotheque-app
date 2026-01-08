-- Script de création des tables pour la bibliothèque universitaire
-- Base de données: bibliothequeuniv

-- Suppression des tables existantes (dans l'ordre des dépendances)
DROP TABLE IF EXISTS emprunt CASCADE;
DROP TABLE IF EXISTS livre CASCADE;
DROP TABLE IF EXISTS etudiant CASCADE;

-- Table etudiant
CREATE TABLE etudiant (
    id_etud SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    date_inscription DATE DEFAULT CURRENT_DATE,
    solde_amende DECIMAL(10,2) DEFAULT 0
);

-- Table livre
CREATE TABLE livre (
    isbn VARCHAR(20) PRIMARY KEY,
    titre VARCHAR(255) NOT NULL,
    editeur VARCHAR(200) NOT NULL,
    annee INTEGER,
    exemplaires_dispo INTEGER DEFAULT 1,
    CHECK (annee IS NULL OR (annee >= 1000 AND annee <= EXTRACT(YEAR FROM CURRENT_DATE)))
);

-- Table emprunt
CREATE TABLE emprunt (
    id_emprunt SERIAL PRIMARY KEY,
    id_etud INTEGER NOT NULL REFERENCES etudiant(id_etud) ON DELETE RESTRICT,
    isbn VARCHAR(20) NOT NULL REFERENCES livre(isbn) ON DELETE RESTRICT,
    date_emprunt DATE NOT NULL DEFAULT CURRENT_DATE,
    date_retour DATE,
    amende DECIMAL(10,2) DEFAULT 0,
    CHECK (date_retour IS NULL OR date_retour >= date_emprunt)
);

-- Index pour améliorer les performances des recherches
CREATE INDEX idx_etudiant_nom ON etudiant(nom);
CREATE INDEX idx_etudiant_email ON etudiant(email);
CREATE INDEX idx_livre_titre ON livre(titre);
CREATE INDEX idx_livre_editeur ON livre(editeur);
CREATE INDEX idx_emprunt_etudiant ON emprunt(id_etud);
CREATE INDEX idx_emprunt_livre ON emprunt(isbn);
CREATE INDEX idx_emprunt_date_retour ON emprunt(date_retour);

-- Commentaires sur les tables
COMMENT ON TABLE etudiant IS 'Table des étudiants inscrits à la bibliothèque';
COMMENT ON TABLE livre IS 'Catalogue des livres disponibles';
COMMENT ON TABLE emprunt IS 'Historique des emprunts de livres';

-- Commentaires sur les colonnes importantes
COMMENT ON COLUMN emprunt.date_retour IS 'NULL si le livre n''est pas encore retourné';
COMMENT ON COLUMN etudiant.solde_amende IS 'Total des amendes dues par l''étudiant';
COMMENT ON COLUMN livre.exemplaires_dispo IS 'Nombre d''exemplaires disponibles';

-- Afficher un message de confirmation
SELECT 'Tables créées avec succès!' AS message;
