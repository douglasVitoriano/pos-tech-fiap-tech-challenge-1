--tabela user
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    full_name TEXT,
    email TEXT,
    hashed_password TEXT
);
