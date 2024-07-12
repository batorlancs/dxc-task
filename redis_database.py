import redis
import utils
from redis.commands.json.path import Path
from typing import Optional
from api_token import ApiToken, ApiTokenData, TokenHandler
from errors import ServerError, AuthenticationError, ForbiddenError


DEFAULT_MAX_TIME_SECONDS = 15
ROOT_PATH = Path.root_path()


class RedisDatabase:
    def __init__(self, check_connection: bool = False):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        if check_connection:
            print("Checking connection to Redis...")
            if not self.check_connection():
                print("Failed.")
                raise ServerError('Could not connect to Redis.')
            else:
                print("Successful.")
        
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

    async def create_token(self, api_token: Optional[ApiToken] = ApiToken()):
        """
        Create a token in Redis with the given access count and limit.

        Args:
            token (str): The token to create.
            access_count (int): The number of times the token has been accessed.
            access_limit (int): The maximum number of times the token can be accessed.
        """
        start_timestamp = self.get_timestamp_seconds()
        token_str = api_token.get_token_str()

        while True:
            if self.is_timeout(start_timestamp):
                raise ServerError('Operation timed out. Please try again later.')

            try:
                # Watch the token for changes
                self.r.watch(token_str)

                if (int(self.r.exists(token_str)) == 1):
                    raise ServerError('Token already exists.')

                self.r.json().set(token_str, ROOT_PATH, api_token.data.__dict__)
                break

            except redis.WatchError:
                # If a WatchError is raised, it means that the watched key was modified
                # by another client before the transaction could be completed. In this
                # case, retry the operation.
                self.r.unwatch()
                continue
            
            finally:
                self.r.unwatch()

    async def delete_token(self, token: str, throw_error_on_not_found: bool = True):
        """
        Delete a token from Redis.

        Args:
            token (str): The token to delete.
        """
        # 1: deleted existing, 0: does not exist
        result = self.r.delete(TokenHandler.format(token))
        if throw_error_on_not_found and result == 0:
            raise ServerError('Token does not exist.')

    async def token_exists(self, token: str) -> bool:
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

    async def get_and_use_token(self, token: str, url: str) -> ApiToken:
        """
        Use a token in Redis.

        Args:
            token (str): The token to use.
        """
        token_str = TokenHandler.format(token)
        start_timestamp = self.get_timestamp_seconds()

        
        while True:
            if self.is_timeout(start_timestamp):
                raise ServerError('Operation timed out. Please try again later.')

            try:
                # Watch the token for changes
                self.r.watch(token_str)

                # Fetch current values
                token_data = self.r.json().get(token_str)

                if not token_data:
                    raise AuthenticationError('Token does not exist.')

                if not utils.is_endpoint_in_any_scope(url, token_data['scopes']):
                    raise ForbiddenError('Token is not authorized to access this endpoint.')

                token_data['access_count'] += 1
                if token_data['access_count'] >= token_data['access_limit']:
                    self.r.delete(token_str)
                else:
                    self.r.json().numincrby(token_str, 'access_count', 1)

                return ApiToken(token, ApiTokenData(**token_data))

            except redis.WatchError:
                # If a WatchError is raised, it means that the watched key was modified
                # by another client before the transaction could be completed. In this
                # case, retry the operation.
                self.r.unwatch()
                continue
            
            finally:
                self.r.unwatch()
