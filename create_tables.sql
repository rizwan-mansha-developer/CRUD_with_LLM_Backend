-- Run this as postgres superuser to create tables manually
-- psql -U postgres -d finance_db -f create_tables.sql

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS expenses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    amount FLOAT NOT NULL,
    category VARCHAR NOT NULL,
    date DATE NOT NULL
);

-- Grant permissions to finance_user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO finance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO finance_user;