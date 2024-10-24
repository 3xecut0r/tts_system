from random import choice

from motor.motor_asyncio import AsyncIOMotorDatabase
import json


class DatabaseService:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._db = db

    async def add_keys_bulk(self, keys_data):
        try:
            result = await self._db.keys.insert_many(keys_data)
            return result.inserted_ids
        except Exception as e:
            raise Exception(f'Error inserting keys into database: {e}')

    async def add_proxy(self, proxy_data):
        try:
            result = await self._db.proxy.insert_one(proxy_data)
            return result.inserted_id
        except Exception as e:
            raise Exception(f'Error inserting proxy into database: {e}')

    async def get_proxy(self):
        try:
            proxies = await self._db.proxy.find().to_list(length=1000)
            if proxies:
                return choice(proxies)
            else:
                raise Exception('No proxies found in the database')
        except Exception as e:
            raise Exception(f'Error retrieving proxy from database: {e}')


def load_keys_in_batches(file_path, batch_size=100):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for i in range(0, len(data), batch_size):
            yield data[i:i + batch_size]

def load_proxies_from_file(file_path):
    proxies = []
    with open(file_path, 'r') as file:
        for line in file:
            proxy = line.strip()
            if proxy:
                ip, port, login, password = proxy.split(':')
                proxies.append({
                    'proxy': f'{ip}:{port}',
                    'login': login,
                    'password': password
                })
    return proxies
