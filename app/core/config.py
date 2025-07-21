from dotenv import load_dotenv
load_dotenv()
import os

#  Database configuration
db_config = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", "postgres"),
    "database": os.getenv("DB_NAME", "job_hunter"),
}

if not all(db_config.values()):
    raise ValueError("Missing database configuration")

SQLALCHEMY_DATABASE_URL = f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}" 

#  Logging configuration

# LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# #  OpenAI configuration

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")