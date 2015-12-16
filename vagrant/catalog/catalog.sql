-- Database definition for Catalog project
-- Add table and view definitions in here and populate
-- required startup

DROP DATABASE catalog;

CREATE DATABASE catalog;

\c catalog;

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL DEFAULT '',
    category_description TEXT
);

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    category_id INT REFERENCES category ON DELETE CASCADE,
    product_name TEXT NOT NULL DEFAULT '',
    product_description TEXT NOT NULL DEFAULT '',
    price NUMERIC(12,2)
);

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    registered TIMESTAMP
);

INSERT INTO category (category_name, category_description) VALUES
    ('Pool Equipment', 'Category for Pool Equipment'),
    ('Garden Equipment', 'Category for Garden Equipment'),
    ('Toys', 'Kids Toys');

INSERT INTO products (category_id,product_name,product_description,price) VALUES
    (1,'Dragon Toy','Kids Pool toy - Children over 10','15.15'),
    (2,'Cricket Set','Kids Cricket set','25.25'),
    (3,'Kylo Ren Mask','Voice Changing Kylo Ren Mask','39.35'),
    (3,'Lightsaber','Light Side Lightsaber (Luke)','85.35'),
    (3,'Lightsaber','Dark Side Lightsaber (Darth Vader)','75.35'),
    (1,'Dive Sticks','Illuminated Dive Sticks (Lightsabers)','65.65'),
    (1,'Dive Mask','Kids Dive Mask (Small)','35.35'),
    (2,'Rocket Launcher','Launches Foam Rockets','32.31'),
    (2,'Growing Eggs','Dinosaur Eggs for Garden','33.32'),
    (2,'Boomerang','Soft Foam Boomerang','37.37'),
    (3,'Adventure Kit','Kids exploration kit - telescope, compass, etc','55.35'),
    (1,'Gup-C','Octonauts pool set','55.35'),
    (1,'Flutter Board','Swimming helper','15.35'),
    (1,'Squirters','Foam squirt guns','5.00'),
    (2,'Squirt Guns','Waterpistols','3.35'),
    (3,'Nerf Guns','For bigger kids','25.35');
