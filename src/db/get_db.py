from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from dotenv import dotenv_values

class Database:
    _client: AsyncIOMotorClient | None = None
    _db: AsyncIOMotorDatabase | None = None

    @staticmethod
    def connect(db_name: str = None) -> None:
        config = dotenv_values('.env')
        Database._client = AsyncIOMotorClient(config['ATLAS_URI'])
        Database._db = Database._client[db_name] if db_name else Database._client[config['DB_NAME']]

    @staticmethod
    def close() -> None:
        if Database._client is not None:
            Database._client.close()
        else:
            raise ConnectionError('Client not connected')

    @staticmethod
    def get_db() -> AsyncIOMotorDatabase:
        if Database._db is not None:
            return Database._db
        else:
            raise ConnectionError('Database not connected')
