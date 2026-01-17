import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
TEST_DB_NAME = "gas_control_test_db"

class TestDB:
    ASYNC_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
    
    SYNC_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
    
    SYSTEM_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
