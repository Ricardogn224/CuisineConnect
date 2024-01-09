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

CREATE TABLE IF NOT EXISTS preferences_utilisateur (
    id_preference INTEGER PRIMARY KEY AUTOINCREMENT,
    id_utilisateur INTEGER NOT NULL,
    preference_type VARCHAR(50),
    valeur VARCHAR(255),
    FOREIGN KEY (id_utilisateur) REFERENCES users(id)
);

INSERT INTO preferences_utilisateur (id_utilisateur, preference_type, valeur)
VALUES (1, 'Allergie', 'Arachides');



