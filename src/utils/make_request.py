import aiohttp
from fake_http_header import FakeHttpHeader
import random
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('LOGGER - ')

async def get_voices(api_key: str = '', proxy: str = ''):
    headers = FakeHttpHeader(
        domain_code=random.choice(['de', 'uk', 'nl', 'fr', 'it', 'ch', 'pl', 'be', 'se'])).as_header_dict()
    headers['xi-api-key'] = api_key

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.elevenlabs.io/v1/voices', headers=headers, proxy=proxy) as response:
            if response.status == 200:
                data = await response.json()
                voices = data.get('voices', [])
                # logger.info(voices)
                for elem in voices:
                    logger.info(f"{elem['name']}: {elem['voice_id']}")
            else:
                logger.info(f'Request failed with status {response.status}')
