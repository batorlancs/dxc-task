import sys
from loguru import logger
from socketify import App
from redis_database import RedisDatabase
from api_token import ApiToken, ApiTokenData


async def setup_empty_db_environment(app: App, db: RedisDatabase):
    logger.warning("Clearing up the database...")
    try:
        await db.clear_all_tokens()
    except Exception as e:
        logger.error(f"Error setting up the empty db environment: {e}")
        logger.info("Exiting the server...")
        sys.exit()


async def setup_test_environment(app: App, db: RedisDatabase):
    logger.warning("Setting up the test environment...")
    try:
        await db.clear_all_tokens()
        # create a admin token to access all the APIs, 10 access limit
        await db.create_token(
            ApiToken("admin10", ApiTokenData(
                access_limit=10,
                access_count=0,
                scopes=["*"]
            )))
        
        # create a admin token to access all the APIs, 5 access limit
        await db.create_token(
            ApiToken("admin5", ApiTokenData(
                access_limit=5,
                access_count=0,
                scopes=["*"]
            )))
        
    except Exception as e:
        logger.error(f"Error setting up the test environment: {e}")
        logger.info("Exiting the server...")
        sys.exit()
    
    