
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS basket_vegetables;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash VARCHAR(128) NOT NULL,
    activity VARCHAR(15) NOT NULL,
    totp varchar(32)
);

CREATE TABLE basket_vegetables(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50) NOT NULL UNIQUE,
    information VARCHAR(128) NOT NULL,
    price INTEGER NOT NULL,
    creator VARCHAR(128) NOT NULL,
    FOREIGN KEY (creator) REFERENCES users(email)
);

CREATE TABLE reservations(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sponsor VARCHAR(128) NOT NULL,
    basket VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL,
    jour date not null, 
    FOREIGN KEY (sponsor) REFERENCES users(email)
    FOREIGN KEY (basket) REFERENCES basket_vegetables(title)
);