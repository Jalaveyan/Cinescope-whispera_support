import os
from dotenv import load_dotenv

load_dotenv(override=True)

class PostgresCredentials:

    USERNAME = os.getenv('USERNAME')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    DATABASE = os.getenv('DB_NAME')
    PORT = os.getenv('PORT')