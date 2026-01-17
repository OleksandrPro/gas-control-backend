import os
import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from tests.constants import TestDB, TEST_DB_NAME

sys.path.append(os.getcwd())

def create_test_db():
    print(f"Connecting to system database...")
    
    try:
        con = psycopg2.connect(TestDB.SYSTEM_URL)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = con.cursor()
        
        cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{TEST_DB_NAME}'")
        exists = cursor.fetchone()
        
        if not exists:
            print(f"Creating database {TEST_DB_NAME}...")
            cursor.execute(f"CREATE DATABASE {TEST_DB_NAME}")
            print("Database created successfully.")
        else:
            print(f"Database {TEST_DB_NAME} already exists.")
            
        cursor.close()
        con.close()
        
    except Exception as e:
        print(f"Error setting up test database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    create_test_db()