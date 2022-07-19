from models.ranking import Ranking

# TODO: move DBMS config to secrets file/config file

def get_database():
    return PostgresDatabase()

# Interface
class Database:
    def connect(self): pass
    def add_fighter_from_ranking(self,ranking: Ranking): pass

# PostgresDatabase
import psycopg2, psycopg2.extras

class PostgresDatabase(Database):
    def connect(self):
        self.connection = psycopg2.connect(
            database="ufc",
            user="jacobgoldfarb", 
            password="", host="127.0.0.1", 
            port="5432"
            )
        self.cursor = self.connection.cursor()
    
    def add_fighter_from_ranking(self,ranking: Ranking):
        sql_values = self.marshall_rankings_for_db(ranking)

        sql_query = "INSERT INTO fighters (full_name, division, ranking) VALUES %s ON CONFLICT (division, ranking) DO NOTHING;"
        psycopg2.extras.execute_values (
            self.cursor, sql_query, sql_values, template=None, page_size=100
        )
        # self.cursor.execute(sql_query)
        self.connection.commit()

    def marshall_rankings_for_db(self, ranking) -> str:
        fighters = ranking.ordered_fighters
        values = zip(
            fighters, 
            [ranking.division  for i in range(len(fighters))],
            [i for i in range(1, len(fighters) + 1)], 
            )
        return list(values)
        