import redis
import utils
from loguru import logger
from redis.commands.json.path import Path
from typing import Optional
from api_token import ApiToken, ApiTokenData, TokenHandler
from errors import ServerError, AuthenticationError, ForbiddenError


DEFAULT_MAX_TIME_SECONDS = 2
DEFAULT_MAX_RETRIES = 10
ROOT_PATH = Path.root_path()


class RedisDatabaseManager:
    def __init__(self, check_connection: bool = False):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        if check_connection:
            if not self.check_connection():
                raise ServerError('Could not connect to Redis.')

    def check_connection(self) -> bool:
        try:
            self.r.ping()
            return True
        except redis.ConnectionError:
            return False

    # Get the current timestamp in seconds
    def get_timestamp_seconds(self) -> int:
        return self.r.time()[0]

    # Check if the operation has timed out
    def is_timeout(self, start_timestamp_seconds: int, max_time_seconds: int = DEFAULT_MAX_TIME_SECONDS) -> bool:
        return self.get_timestamp_seconds() - start_timestamp_seconds > max_time_seconds

    def clear_all_tokens(self):
        """
        Clear all tokens in Redis.
        """
        self.r.flushall()
        logger.debug("All tokens cleared (database flushed).")

    def create_token(self, api_token: Optional[ApiToken] = ApiToken()) -> ApiToken:
        """
        Create a token in Redis with the given access count and limit.

        Args:
            token (str): The token to create.
            access_count (int): The number of times the token has been accessed.
            access_limit (int): The maximum number of times the token can be accessed.
        """
        start_timestamp = self.get_timestamp_seconds()
        token_str = api_token.get_token_str()
        max_retries = DEFAULT_MAX_RETRIES
        curr_retries = 0

        # validate the token attributes
        if not api_token.validate():
            raise ServerError('Token data is not valid, please check the data provided.')

        while True:
            with self.r.pipeline() as pipe:
                if self.is_timeout(start_timestamp):
                    raise ServerError('Operation timed out. Please try again later.')

                pipe.multi()
                pipe.json().set(token_str, ROOT_PATH, api_token.data.__dict__)
                pipe.json().get(token_str)
                res = pipe.execute()
                logger.debug(res)

                pipe_success = res[0] and res[1] is not None

                # This is in case the same client is trying to use the token multiple times asynchronously
                if not pipe_success:
                    if curr_retries < max_retries:
                        curr_retries += 1
                        logger.error(f"...Retrying to create token: {token_str}")
                        continue
                    else:
                        raise ServerError('Token creation failed.')

                logger.debug(f"Token created: {token_str}")
                return ApiToken.from_dict({'token': token_str, 'data': res[1]})
            
    def delete_token(self, token: str):
        """
        Delete a token from Redis.

        Args:
            token (str): The token to delete.
        """
        # 1: deleted existing, 0: does not exist
        result = self.r.delete(TokenHandler.format(token))
        if result == 0:
            logger.debug(f"Token delete, does not exist: {token}")
        
        logger.debug(f"Token delete, success: {token}")

    def token_exists(self, token: str) -> bool:
        """
        Check if a token exists in Redis.

        Args:
            token (str): The token to check.

        Returns:
            bool: True if the token exists, False otherwise.
        """
        num_exists = self.r.exists(TokenHandler.format(token))
        if num_exists == 0:
            return False

        return True

    def get_and_use_token(self, token: str, url: str = None) -> ApiToken:
        """
        Use a token in Redis.

        Args:
            token (str): The token to use.
        """
        token_str = TokenHandler.format(token)
        start_timestamp = self.get_timestamp_seconds()
        max_retries = DEFAULT_MAX_RETRIES
        curr_retries = 0

        while True:
            with self.r.pipeline() as pipe:
                if self.is_timeout(start_timestamp):
                    raise ServerError('Operation timed out. Please try again later.')

                try:
                    # Watch the token for changes
                    pipe.watch(token_str)

                    # Fetch current values
                    token_data = pipe.json().get(token_str)

                    if not token_data:
                        raise AuthenticationError('Token is not valid.')

                    if url and not utils.is_endpoint_in_any_scope(url, token_data['scopes']):
                        raise ForbiddenError('Token is not authorized to access this endpoint.')

                    reached_access_limit = token_data['access_count'] + 1 >= token_data['access_limit']
                    pipe.multi()  # Start multi transaction
                    pipe.json().numincrby(token_str, 'access_count', 1)  # Increment access count
                    pipe.json().get(token_str)  # Get updated token data

                    # Delete token if access limit is reached
                    if reached_access_limit:
                        pipe.delete(token_str)

                    pipe.unwatch()
                    res = pipe.execute()  # Execute multi transaction

                    logger.debug(res)

                    # Check if the transaction was successful
                    pipe_success_when_inc = len(res) == 3 and res[0] >= 1 and res[1] is not None and res[2]
                    pipe_success_when_del = len(res) == 4 and res[0] >= 1 and res[1] is not None and res[2] == 1 and res[3]
                    pipe_success = pipe_success_when_del if reached_access_limit else pipe_success_when_inc

                    # This is in case the same client is trying to use the token multiple times asynchronously
                    if not pipe_success:
                        if curr_retries < max_retries:
                            curr_retries += 1
                            logger.error(f"Pipeline error, retrying to use token: {token_str}")
                            continue
                        else:
                            raise ServerError('Token usage failed.')

                    logger.debug(f"Token used: {token_str}, with current access_count: {res[1]['access_count']}")
                    return ApiToken.from_dict({'token': token_str, 'data': res[1]})

                except redis.WatchError:
                    # If a WatchError is raised, it means that the watched key was modified
                    # by another client before the transaction could be completed. In this
                    # case, retry the operation.
                    pipe.unwatch()
                    logger.error(f"Token watch error: {token_str}")
                    continue
            


db = RedisDatabaseManager()
