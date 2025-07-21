from app.db.session import init_db
from app.core.config import db_config
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db_if_not_exists(db_config):
    conn = psycopg2.connect(
        host=db_config["host"],
        port=db_config["port"],
        user=db_config["user"],
        password=db_config["password"],
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Check if database exists
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_config["database"],))
    exists = cur.fetchone()
    if not exists:
        # Create database
        cur.execute(f"CREATE DATABASE {db_config['database']}")
        print(f"Database {db_config['database']} created successfully")
    else:
        print(f"Database {db_config['database']} already exists")
    cur.close()
    conn.close()



try:
    create_db_if_not_exists(db_config)
    init_db()
    print("Database initialized successfully")
except Exception as e:
    print(f"Error initializing database: {e}")