from .postgres_db import PostgresDatabase
_database = PostgresDatabase() 

def get_database():
    return _database
