from models.ranking import Ranking
from .secrets import get_secrets

class Config:
    db_name: str
    host: str
    port: str
    user: str
    password: str
    
    def __init__(self):
        config_info = get_secrets()
        self.db_name = config_info.get('DB_NAME')
        self.host = config_info.get('DB_HOST')
        self.port = config_info.get('DB_PORT')
        self.user = config_info.get('DB_USER')
        self.password = config_info.get('DB_PASSWORD'),

class Database:
        
    def __init__(self):
        config = Config()
        self.connection = self.connect(config)
        self.cursor = self.connection.cursor()
        
    def __del__(self):
        self.cursor.close()
        self.connection.close()
        
    def connect(self): raise NotImplementedError
    def add_fighter_from_rankings(self, ranking: Ranking): raise NotImplementedError