-- Connect to PostgreSQL as superuser (postgres) and run these commands:

-- Grant necessary permissions to the finance_user
GRANT CREATE ON SCHEMA public TO finance_user;
GRANT USAGE ON SCHEMA public TO finance_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO finance_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO finance_user;

-- Alternative: Make finance_user owner of the database
ALTER DATABASE finance_db OWNER TO finance_user;

-- Or create the user with proper permissions from start:
-- DROP USER IF EXISTS finance_user;
-- CREATE USER finance_user WITH PASSWORD 'secret' CREATEDB;
-- CREATE DATABASE finance_db OWNER finance_user;