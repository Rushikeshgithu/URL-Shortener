DROP TABLE IF EXISTS urls;

CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_code TEXT UNIQUE NOT NULL
);