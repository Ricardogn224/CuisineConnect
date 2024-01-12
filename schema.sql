CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pseudo VARCHAR (255) NOT NULL,
    email VARCHAR (255) NOT NULL,
    password VARCHAR (255) NOT NULL,
    adresse VARCHAR (255) NOT NULL,
    telephone VARCHAR (255) NOT NULL,   
    UNIQUE (email)
);

CREATE TABLE IF NOT EXISTS recettes (
    id_recette INTEGER PRIMARY KEY AUTOINCREMENT,
    titre VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    instructions VARCHAR(255),
    pays VARCHAR(255),
    temps_preparation INTEGER,
    image VARCHAR(255),
    id_utilisateur INTEGER NOT NULL,
    nombre_personnes INTEGER,
    ingredients_disponibles VARCHAR(255),
    FOREIGN KEY (id_utilisateur) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS ingredients (
    id_ingredient INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_ingredient VARCHAR(255),
    quantite DECIMAL(10,2),
    unite_mesure VARCHAR(50),
    id_recette INTEGER NOT NULL,
    FOREIGN KEY (id_recette) REFERENCES recettes(id_recette)
);


CREATE TABLE IF NOT EXISTS recettes_favoris (
    id_favori INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    id_recette INTEGER NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES users(id),
    FOREIGN KEY (id_recette) REFERENCES recettes(id_recette)
);

CREATE TABLE IF NOT EXISTS recettes_notes (
    id_note INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    id_recette INTEGER NOT NULL,
    note INTEGER NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES users(id),
    FOREIGN KEY (id_recette) REFERENCES recettes(id_recette)
);

CREATE TABLE IF NOT EXISTS recettes_commentaires (
    id_commentaire INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    id_recette INTEGER NOT NULL,
    FOREIGN KEY (id_utilisateur) REFERENCES users(id),
    FOREIGN KEY (id_recette) REFERENCES recettes(id_recette)
);

CREATE TABLE IF NOT EXISTS preferences_utilisateur (
    id_preference INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    preference_type VARCHAR(50),
    valeur VARCHAR(255),
    FOREIGN KEY (id_utilisateur) REFERENCES users(id)
);

INSERT INTO users (pseudo, email, password, adresse, telephone) VALUES ('ChefAfricain', 'chefafricain@example.com', 'password123', '123 Rue Afrique', '9876543210');

INSERT INTO recettes (titre, description, instructions, pays, temps_preparation, image, id_utilisateur, nombre_personnes, ingredients_disponibles) VALUES
('Yassa', 'Poulet Yassa du Sénégal', 'Instructions...', 'Sénégal', 60, 'yassa.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 4, 'Ingredients for Yassa available'),
('Jollof Rice', 'Riz Jollof', 'Instructions...', 'Nigeria', 50, 'jollof_rice.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 6, 'Ingredients for Jollof Rice available'),
('Couscous', 'Couscous traditionnel', 'Instructions...', 'Maroc', 90, 'couscous.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 5, 'Ingredients for Couscous available'),
('Bobotie', 'Bobotie d''Afrique du Sud', 'Instructions...', 'Afrique du Sud', 80, 'bobotie.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 8, 'Ingredients for Bobotie available'),
('Fufu et Soup', 'Fufu et sa soup', 'Instructions...', 'Ghana', 70, 'fufu_soup.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 3, 'Ingredients for Fufu and Soup available'),
('Maafe', 'Maafe', 'Instructions...', 'Mali', 85, 'maafe.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 4, 'Ingredients for Maafe available'),
('Chapati', 'Chapati kényan', 'Instructions...', 'Kenya', 30, 'chapati.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 2, 'Ingredients for Chapati available'),
('Injera et Ragoût', 'Injera avec ragoût', 'Instructions...', 'Éthiopie', 90, 'injera_stew.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 4, 'Ingredients for Injera and Stew available'),
('Mozzarella et Akara', 'Sandwich Mozzarella et Akara', 'Instructions...', 'Nigeria', 45, 'mozzarella_akara.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 2, 'Ingredients for Mozzarella and Akara available'),
('Bunny Chow', 'Bunny Chow d''Afrique du Sud', 'Instructions...', 'Afrique du Sud', 60, 'bunny_chow.jpg', (SELECT id FROM users WHERE pseudo = 'ChefAfricain'), 3, 'Ingredients for Bunny Chow available');

-- Ingrédients pour la recette Yassa
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Poulet', 1.5, 'kg', 1),
('Oignons', 0.5, 'kg', 1),
('Citron', 2, 'unité', 1);

-- Ingrédients pour la recette Jollof Rice
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Riz', 1, 'kg', 2),
('Tomates', 0.5, 'kg', 2),
('Poivrons', 0.2, 'kg', 2);

-- Ingrédients pour la recette Couscous
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Semoule de couscous', 1, 'kg', 3),
('Légumes variés', 0.5, 'kg', 3),
('Agneau', 1, 'kg', 3);

-- Ingrédients pour la recette Bobotie
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Boeuf haché', 1, 'kg', 4),
('Pain', 0.2, 'kg', 4),
('Lait', 0.25, 'litre', 4);

-- Ingrédients pour la recette Fufu et Soup
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Manioc', 1, 'kg', 5),
('Poulet', 0.5, 'kg', 5),
('Légumes', 0.3, 'kg', 5);

-- Ingrédients pour la recette Maafe
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Poulet', 1, 'kg', 6),
('Pâte d''arachide', 0.2, 'kg', 6),
('Tomates', 0.3, 'kg', 6);

-- Ingrédients pour la recette Chapati
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Farine', 0.5, 'kg', 7),
('Eau', 0.25, 'litre', 7),
('Huile', 0.05, 'litre', 7);

-- Ingrédients pour la recette Injera et Ragoût
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Farine de teff', 0.5, 'kg', 8),
('Eau', 0.5, 'litre', 8),
('Boeuf', 0.7, 'kg', 8);

-- Ingrédients pour la recette Mozzarella et Akara
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Haricots noirs', 0.3, 'kg', 9),
('Mozzarella', 0.2, 'kg', 9),
('Huile', 0.1, 'litre', 9);

-- Ingrédients pour la recette Bunny Chow
INSERT INTO ingredients (nom_ingredient, quantite, unite_mesure, id_recette) VALUES
('Pain', 1, 'unité', 10),
('Curry', 0.05, 'kg', 10),
('Poulet', 0.5, 'kg', 10);


INSERT INTO recettes_favoris (id_utilisateur, id_recette) VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7),
(4, 8);

INSERT INTO recettes_favoris (id_utilisateur, id_recette) VALUES
(1, 10),
(1, 2),
(2, 3),
(2, 4),
(3, 5),
(3, 6),
(4, 7),
(4, 8);

INSERT INTO preferences_utilisateur (id_utilisateur, preference_type, valeur) VALUES
(1, 'Allergie', 'Arachides'),
(1, 'Régime', 'Végétarien'),
(2, 'Allergie', 'Gluten'),
(2, 'Régime', 'Vegan'),
(3, 'Allergie', 'Lactose'),
(3, 'Régime', 'Sans gluten'),
(4, 'Allergie', 'Fruits de mer'),
(4, 'Régime', 'Paléo');




