import sys
from loguru import logger
from db.db_manager import db
from api_token import ApiToken, ApiTokenData


class InvalidArgumentError(Exception):
    """Exception to handle invalid arguments"""
    pass


class EnvironmentSetupError(Exception):
    """Exception to handle all errors happening when setting up the environment"""
    pass


async def setup_environment_with_args(args: list):
    """
    Setup the environment based on the arguments given in the command line.
    Use --test to setup the test environment.
    Use --empty to setup the empty environment.

    Args:
        args (list): The list of arguments.

    Raises:
        InvalidArgumentError: If the argument is invalid.
        EnvironmentSetupError: If there is an error setting up the environment.
    """
    if len(args) == 2:
        if args[1] == "--test":
            logger.warning("Setting up the test environment...")
            await setup_test_environment()
            logger.info("Test environment setup complete.")
        elif args[1] == "--empty":
            logger.warning("Setting up the empty environment...")
            await setup_empty_db_environment()
            logger.info("Empty environment setup complete.")
        else:
            raise InvalidArgumentError("Invalid environment argument. Try using --test or --empty.")
    elif len(args) > 2:
        raise InvalidArgumentError("Invalid number of arguments. Try using just --test or --empty.")
    else:
        logger.info("Using the default environment...")


async def setup_empty_db_environment():
    try:
        await db.clear_all_tokens()
    except Exception as e:
        raise EnvironmentSetupError(f"Error setting up the empty database environment: {e}")


async def setup_test_environment():
    try:
        await db.clear_all_tokens()

        # create a admin token to access all the APIs, 5 access limit
        await db.create_token(
            ApiToken("admin5", ApiTokenData(
                access_limit=5,
                access_count=0,
                scopes=["*"]
            )))

        # create a admin token to access all the APIs, 10 access limit
        await db.create_token(
            ApiToken("admin10", ApiTokenData(
                access_limit=10,
                access_count=0,
                scopes=["*"]
            )))

        # create a admin token to access all the APIs, 100 access limit
        await db.create_token(
            ApiToken("admin100", ApiTokenData(
                access_limit=100,
                access_count=0,
                scopes=["*"]
            )))

        # create a admin token to access all the APIs, 1000 access limit
        await db.create_token(
            ApiToken("admin1000", ApiTokenData(
                access_limit=1000,
                access_count=0,
                scopes=["*"]
            )))

    except Exception as e:
        raise EnvironmentSetupError(f"Error setting up the test environment: {e}")
