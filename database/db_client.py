import psycopg2
from resources import db_creds
from resources.db_creds import PostgresCredentials


def connect_to_postgres():

    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(
            host=PostgresCredentials.HOST,
            database=PostgresCredentials.DATABASE,
            user=PostgresCredentials.USERNAME,
            password=PostgresCredentials.PASSWORD,
            port=PostgresCredentials.PORT
        )

        print("Connected to PostgreSQL")
        cursor = connection.cursor()

        print("Information about the server")
        print(connection.get_dsn_parameters(), "\n")

        cursor.execute("SELECT version();")

        record = cursor.fetchone()
        print("You are connected to Postgres database", record, "\n")

    except Exception as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    connect_to_postgres()