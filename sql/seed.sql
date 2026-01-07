-- Données de test pour la bibliothèque universitaire
-- À exécuter après init.sql

-- Nettoyage des données existantes
TRUNCATE TABLE emprunt CASCADE;
TRUNCATE TABLE livre RESTART IDENTITY CASCADE;
TRUNCATE TABLE etudiant RESTART IDENTITY CASCADE;

-- Insertion d'étudiants
INSERT INTO etudiant (nom, prenom, email) VALUES
    ('Dupont', 'Jean', 'jean.dupont@supdevinci.fr'),
    ('Martin', 'Sophie', 'sophie.martin@supdevinci.fr'),
    ('Bernard', 'Luc', 'luc.bernard@supdevinci.fr'),
    ('Petit', 'Marie', 'marie.petit@supdevinci.fr'),
    ('Durand', 'Pierre', 'pierre.durand@supdevinci.fr'),
    ('Moreau', 'Julie', 'julie.moreau@supdevinci.fr'),
    ('Leroy', 'Thomas', 'thomas.leroy@supdevinci.fr'),
    ('Simon', 'Emma', 'emma.simon@supdevinci.fr'),
    ('Laurent', 'Lucas', 'lucas.laurent@supdevinci.fr'),
    ('Michel', 'Chloé', 'chloe.michel@supdevinci.fr');

-- Insertion de livres
INSERT INTO livre (titre, auteur, annee_publication) VALUES
    -- Classiques français
    ('Le Petit Prince', 'Antoine de Saint-Exupéry', 1943),
    ('Les Misérables', 'Victor Hugo', 1862),
    ('L''Étranger', 'Albert Camus', 1942),
    ('Madame Bovary', 'Gustave Flaubert', 1857),
    ('Le Comte de Monte-Cristo', 'Alexandre Dumas', 1844),

    -- Classiques anglais/américains
    ('1984', 'George Orwell', 1949),
    ('To Kill a Mockingbird', 'Harper Lee', 1960),
    ('The Great Gatsby', 'F. Scott Fitzgerald', 1925),
    ('Pride and Prejudice', 'Jane Austen', 1813),
    ('Brave New World', 'Aldous Huxley', 1932),

    -- Fantasy/SF
    ('Harry Potter à l''école des sorciers', 'J.K. Rowling', 1997),
    ('Le Seigneur des Anneaux', 'J.R.R. Tolkien', 1954),
    ('Dune', 'Frank Herbert', 1965),
    ('Foundation', 'Isaac Asimov', 1951),
    ('The Hitchhiker''s Guide to the Galaxy', 'Douglas Adams', 1979),

    -- Littérature contemporaine
    ('L''Alchimiste', 'Paulo Coelho', 1988),
    ('Cent ans de solitude', 'Gabriel García Márquez', 1967),
    ('Le Nom de la rose', 'Umberto Eco', 1980),
    ('Americanah', 'Chimamanda Ngozi Adichie', 2013),
    ('Les Bienveillantes', 'Jonathan Littell', 2006),

    -- Informatique/Tech
    ('Clean Code', 'Robert C. Martin', 2008),
    ('The Pragmatic Programmer', 'Andrew Hunt', 1999),
    ('Introduction to Algorithms', 'Thomas H. Cormen', 1990),
    ('Design Patterns', 'Erich Gamma', 1994),
    ('The Phoenix Project', 'Gene Kim', 2013);

-- Insertion d'emprunts (quelques exemples)
-- Emprunts en cours
INSERT INTO emprunt (etudiant_id, livre_id, date_emprunt, date_retour) VALUES
    (1, 1, CURRENT_DATE - INTERVAL '5 days', NULL),
    (2, 6, CURRENT_DATE - INTERVAL '10 days', NULL),
    (3, 11, CURRENT_DATE - INTERVAL '3 days', NULL),
    (4, 21, CURRENT_DATE - INTERVAL '7 days', NULL),
    (5, 15, CURRENT_DATE - INTERVAL '12 days', NULL);

-- Emprunts en retard (plus de 14 jours)
INSERT INTO emprunt (etudiant_id, livre_id, date_emprunt, date_retour) VALUES
    (6, 3, CURRENT_DATE - INTERVAL '20 days', NULL),
    (7, 12, CURRENT_DATE - INTERVAL '18 days', NULL),
    (8, 7, CURRENT_DATE - INTERVAL '25 days', NULL);

-- Emprunts terminés (retournés)
INSERT INTO emprunt (etudiant_id, livre_id, date_emprunt, date_retour) VALUES
    (1, 2, CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE - INTERVAL '16 days'),
    (2, 5, CURRENT_DATE - INTERVAL '25 days', CURRENT_DATE - INTERVAL '11 days'),
    (3, 8, CURRENT_DATE - INTERVAL '45 days', CURRENT_DATE - INTERVAL '31 days'),
    (4, 13, CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE - INTERVAL '8 days'),
    (5, 16, CURRENT_DATE - INTERVAL '35 days', CURRENT_DATE - INTERVAL '22 days'),
    (6, 19, CURRENT_DATE - INTERVAL '40 days', CURRENT_DATE - INTERVAL '28 days'),
    (7, 22, CURRENT_DATE - INTERVAL '50 days', CURRENT_DATE - INTERVAL '38 days'),
    (8, 4, CURRENT_DATE - INTERVAL '60 days', CURRENT_DATE - INTERVAL '48 days'),
    (9, 9, CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE - INTERVAL '3 days'),
    (10, 14, CURRENT_DATE - INTERVAL '28 days', CURRENT_DATE - INTERVAL '15 days');

-- Afficher un résumé
SELECT 'Données insérées avec succès!' AS message;
SELECT COUNT(*) AS nb_etudiants FROM etudiant;
SELECT COUNT(*) AS nb_livres FROM livre;
SELECT COUNT(*) AS nb_emprunts_total FROM emprunt;
SELECT COUNT(*) AS nb_emprunts_en_cours FROM emprunt WHERE date_retour IS NULL;
