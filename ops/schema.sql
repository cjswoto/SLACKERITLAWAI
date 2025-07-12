CREATE TABLE IF NOT EXISTS custodians (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    custodian_id INTEGER REFERENCES custodians(id),
    object_key TEXT NOT NULL,
    subject TEXT,
    body TEXT,
    sent_at TIMESTAMP,
    sha256 TEXT,
    duplicate BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS review_tags (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id),
    tag TEXT
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);
