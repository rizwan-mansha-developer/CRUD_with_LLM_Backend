-- Connect to PostgreSQL as superuser and run these commands:
-- psql -U postgres -d finance_db

-- Grant schema permissions
GRANT CREATE ON SCHEMA public TO finance_user;
GRANT USAGE ON SCHEMA public TO finance_user;

-- Grant table permissions (for existing and future tables)
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO finance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO finance_user;

-- Grant default privileges for future objects
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO finance_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO finance_user;

-- Make finance_user owner of the database (optional but recommended)
ALTER DATABASE finance_db OWNER TO finance_user;