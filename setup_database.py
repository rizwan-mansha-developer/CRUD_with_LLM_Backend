#!/usr/bin/env python3
"""
Database setup script for PostgreSQL
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def create_database_and_user():
    """Create database and user with proper permissions"""
    
    # Connect as superuser (you'll need to modify these)
    POSTGRES_HOST = "localhost"
    POSTGRES_PORT = "5432"
    POSTGRES_SUPERUSER = "postgres"  # Change this to your superuser
    POSTGRES_PASSWORD = "your_postgres_password"  # Change this
    
    try:
        # Connect as superuser
        conn = psycopg2.connect(
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            user=POSTGRES_SUPERUSER,
            password=POSTGRES_PASSWORD,
            database="postgres"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create user if not exists
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'finance_user') THEN
                    CREATE USER finance_user WITH PASSWORD 'secret' CREATEDB;
                END IF;
            END
            $$;
        """)
        
        # Create database if not exists
        cursor.execute("""
            SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'finance_db'
        """)
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute("CREATE DATABASE finance_db OWNER finance_user")
            print("✓ Database 'finance_db' created")
        else:
            print("✓ Database 'finance_db' already exists")
        
        # Grant permissions
        cursor.execute("GRANT ALL PRIVILEGES ON DATABASE finance_db TO finance_user")
        
        cursor.close()
        conn.close()
        
        print("✓ Database setup completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error setting up database: {e}")
        print("\nManual steps:")
        print("1. Connect to PostgreSQL as superuser")
        print("2. Run the commands in fix_postgres_permissions.sql")
        return False

if __name__ == "__main__":
    print("Setting up PostgreSQL database...")
    create_database_and_user()