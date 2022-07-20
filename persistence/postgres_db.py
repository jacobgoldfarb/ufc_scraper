import psycopg2, psycopg2.extras
from .db_interface import Database, Config
from models.ranking import Ranking

class PostgresDatabase(Database):
        
    def connect(self, config: Config):
        return psycopg2.connect(
            database=config.db_name,
            user=config.user, 
            password=config.password,
            host=config.host, 
            port=config.port
            )
    
    def add_fighter_from_rankings(self, rankings: list[Ranking]):
        sql_values = sum([self._marshall_rankings_for_db(ranking) for ranking in rankings], [])
        return self._insert_fighter(sql_values)
    
    # Singular to concurrently "interweave" page parsing and db update in the future.
    def add_fighter_from_ranking(self, ranking: Ranking):
        sql_values = self._marshall_rankings_for_db(ranking)
        return self._insert_fighter(sql_values)
    
    def _insert_fighter(self, values):
        sql_query = """INSERT INTO fighters (full_name, division, ranking) VALUES %s 
        ON CONFLICT (division, ranking) DO NOTHING;"""
        psycopg2.extras.execute_values (
            self.cursor, sql_query, values, template=None, page_size=100
        )
        return self.connection.commit()

    def _marshall_rankings_for_db(self, ranking) -> str:
        ordered_fighters = ranking.ordered_fighters
        num_fighters = len(ordered_fighters)
        values = zip(
            ordered_fighters, 
            [ranking.division  for _ in range(num_fighters)],
            list(range(1,  num_fighters + 1)), 
            )
        return list(values)
        