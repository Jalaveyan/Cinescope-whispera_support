from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import PostgresCredentials

USERNAME = PostgresCredentials.USERNAME
PASSWORD = PostgresCredentials.PASSWORD
HOST = PostgresCredentials.HOST
PORT = PostgresCredentials.PORT
DATABASE = PostgresCredentials.DATABASE

engine = create_engine(
    f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}",
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db_session():
    return SessionLocal()