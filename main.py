from src.db.get_db import Database
from src.utils.manage_data import DatabaseService, load_keys_in_batches

import logging
import asyncio



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LOGGER - ')
PROXIES = []


async def upload_keys():
    Database.connect('keys')
    db = Database.get_db()

    db_service = DatabaseService(db)
    for batch in load_keys_in_batches('src/keys/keys.json', batch_size=100):
        inserted_ids = await db_service.add_keys_bulk(batch)
        logger.info(f'Batch inserted with IDs: {inserted_ids}')
    Database.close()

async def upload_proxies():
    proxies = {}
    with open('Proxy.txt', 'r') as file:
        for line in file:
            print(parse_proxy(line))
    return proxies


def parse_proxy(proxy_str):
    ip, port, login, password = proxy_str.split(':')
    return f'https://{login}:{password}@{ip}:{port}'

async def main():
    proxy_dict = await upload_proxies()
    print(proxy_dict)


if __name__ == '__main__':
    asyncio.run(main())
