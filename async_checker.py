import asyncio
from loguru import logger
from redis_db import db

async def async_checker():
    logger.info("Sdfsdf")
    await db.create_token()
    


if __name__ == "__main__":
    asyncio.run(async_checker())