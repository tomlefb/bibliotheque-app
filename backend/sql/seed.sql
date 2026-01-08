-- Données de test pour la bibliothèque universitaire
-- À exécuter après init.sql

-- Nettoyage des données existantes
TRUNCATE TABLE emprunt CASCADE;
TRUNCATE TABLE livre CASCADE;
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

-- Insertion de livres (avec ISBN)
INSERT INTO livre (isbn, titre, editeur, annee, exemplaires_dispo) VALUES
    -- Classiques français
    ('978-2-07-040850-4', 'Le Petit Prince', 'Gallimard', 1943, 3),
    ('978-2-07-040999-0', 'Les Misérables', 'Gallimard', 1862, 2),
    ('978-2-07-036024-8', 'L''Étranger', 'Gallimard', 1942, 2),
    ('978-2-07-041239-6', 'Madame Bovary', 'Gallimard', 1857, 1),
    ('978-2-07-040826-9', 'Le Comte de Monte-Cristo', 'Gallimard', 1844, 2),

    -- Classiques anglais/américains
    ('978-2-07-036822-0', '1984', 'Gallimard', 1949, 3),
    ('978-2-253-11587-3', 'To Kill a Mockingbird', 'Le Livre de Poche', 1960, 2),
    ('978-2-07-036024-9', 'The Great Gatsby', 'Gallimard', 1925, 1),
    ('978-2-253-00434-4', 'Pride and Prejudice', 'Le Livre de Poche', 1813, 2),
    ('978-2-266-28322-4', 'Brave New World', 'Pocket', 1932, 1),

    -- Fantasy/SF
    ('978-2-07-054602-2', 'Harry Potter à l''école des sorciers', 'Gallimard', 1997, 4),
    ('978-2-267-02700-0', 'Le Seigneur des Anneaux', 'Christian Bourgois', 1954, 2),
    ('978-2-266-23339-7', 'Dune', 'Pocket', 1965, 2),
    ('978-2-07-041239-7', 'Foundation', 'Gallimard', 1951, 1),
    ('978-2-07-046540-8', 'The Hitchhiker''s Guide to the Galaxy', 'Gallimard', 1979, 2),

    -- Littérature contemporaine
    ('978-2-08-070359-5', 'L''Alchimiste', 'Flammarion', 1988, 3),
    ('978-2-02-006070-5', 'Cent ans de solitude', 'Seuil', 1967, 1),
    ('978-2-253-03765-6', 'Le Nom de la rose', 'Le Livre de Poche', 1980, 2),
    ('978-2-07-045421-1', 'Americanah', 'Gallimard', 2013, 1),
    ('978-2-07-034700-3', 'Les Bienveillantes', 'Gallimard', 2006, 1),

    -- Informatique/Tech
    ('978-0-13-235088-4', 'Clean Code', 'Prentice Hall', 2008, 3),
    ('978-0-201-61622-4', 'The Pragmatic Programmer', 'Addison-Wesley', 1999, 2),
    ('978-0-262-03384-8', 'Introduction to Algorithms', 'MIT Press', 1990, 2),
    ('978-0-201-63361-0', 'Design Patterns', 'Addison-Wesley', 1994, 2),
    ('978-0-98826-259-1', 'The Phoenix Project', 'IT Revolution', 2013, 1);

-- Insertion d'emprunts (quelques exemples)
-- Emprunts en cours
INSERT INTO emprunt (id_etud, isbn, date_emprunt, date_retour, amende) VALUES
    (1, '978-2-07-040850-4', CURRENT_DATE - INTERVAL '5 days', NULL, 0),
    (2, '978-2-07-036822-0', CURRENT_DATE - INTERVAL '10 days', NULL, 0),
    (3, '978-2-07-054602-2', CURRENT_DATE - INTERVAL '3 days', NULL, 0),
    (4, '978-0-13-235088-4', CURRENT_DATE - INTERVAL '7 days', NULL, 0),
    (5, '978-2-07-046540-8', CURRENT_DATE - INTERVAL '12 days', NULL, 0);

-- Emprunts en retard (plus de 14 jours)
INSERT INTO emprunt (id_etud, isbn, date_emprunt, date_retour, amende) VALUES
    (6, '978-2-07-036024-8', CURRENT_DATE - INTERVAL '20 days', NULL, 0),
    (7, '978-2-267-02700-0', CURRENT_DATE - INTERVAL '18 days', NULL, 0),
    (8, '978-2-253-11587-3', CURRENT_DATE - INTERVAL '25 days', NULL, 0);

-- Emprunts terminés (retournés)
INSERT INTO emprunt (id_etud, isbn, date_emprunt, date_retour, amende) VALUES
    (1, '978-2-07-040999-0', CURRENT_DATE - INTERVAL '30 days', CURRENT_DATE - INTERVAL '16 days', 0),
    (2, '978-2-07-040826-9', CURRENT_DATE - INTERVAL '25 days', CURRENT_DATE - INTERVAL '11 days', 0),
    (3, '978-2-07-036024-9', CURRENT_DATE - INTERVAL '45 days', CURRENT_DATE - INTERVAL '31 days', 0),
    (4, '978-2-266-23339-7', CURRENT_DATE - INTERVAL '20 days', CURRENT_DATE - INTERVAL '8 days', 0),
    (5, '978-2-08-070359-5', CURRENT_DATE - INTERVAL '35 days', CURRENT_DATE - INTERVAL '22 days', 0),
    (6, '978-2-07-045421-1', CURRENT_DATE - INTERVAL '40 days', CURRENT_DATE - INTERVAL '28 days', 0),
    (7, '978-0-201-61622-4', CURRENT_DATE - INTERVAL '50 days', CURRENT_DATE - INTERVAL '38 days', 0),
    (8, '978-2-07-041239-6', CURRENT_DATE - INTERVAL '60 days', CURRENT_DATE - INTERVAL '48 days', 0),
    (9, '978-2-253-00434-4', CURRENT_DATE - INTERVAL '15 days', CURRENT_DATE - INTERVAL '3 days', 0),
    (10, '978-2-07-041239-7', CURRENT_DATE - INTERVAL '28 days', CURRENT_DATE - INTERVAL '15 days', 0);

-- Mettre à jour les exemplaires disponibles pour les emprunts en cours
UPDATE livre SET exemplaires_dispo = exemplaires_dispo - 1 WHERE isbn IN (
    '978-2-07-040850-4', '978-2-07-036822-0', '978-2-07-054602-2',
    '978-0-13-235088-4', '978-2-07-046540-8', '978-2-07-036024-8',
    '978-2-267-02700-0', '978-2-253-11587-3'
);

-- Afficher un résumé
SELECT 'Données insérées avec succès!' AS message;
SELECT COUNT(*) AS nb_etudiants FROM etudiant;
SELECT COUNT(*) AS nb_livres FROM livre;
SELECT COUNT(*) AS nb_emprunts_total FROM emprunt;
SELECT COUNT(*) AS nb_emprunts_en_cours FROM emprunt WHERE date_retour IS NULL;
