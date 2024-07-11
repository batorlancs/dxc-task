import redis
from redis.commands.json.path import Path
from typing import Optional
from api_token import ApiToken, ApiTokenData, TokenHandler


# Constants
DEFAULT_MAX_TIME_SECONDS = 15
ROOT_PATH = Path.root_path()


class RedisDatabase:
    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        print("Connected to Redis!")
    
    
    def get_timestamp_seconds(self) -> int:
        return self.r.time()[0]


    def is_timeout(self, start_timestamp_seconds: int, max_time_seconds: int = DEFAULT_MAX_TIME_SECONDS) -> bool:
        """
        Check if the operation has timed out.
        
        Args:
            start_timestamp_seconds (int): The start timestamp of the operation.
            max_time_seconds (int): The maximum time allowed for the operation.
            
        Returns:
            bool: True if the operation has timed out, False otherwise.
        """
        return self.get_timestamp_seconds() - start_timestamp_seconds > max_time_seconds


    def create_token(self, api_token: Optional[ApiToken] = ApiToken()):
        """
        Create a token in Redis with the given access count and limit.
        
        Args:
            token (str): The token to create.
            access_count (int): The number of times the token has been accessed.
            access_limit (int): The maximum number of times the token can be accessed.
        """
        start_timestamp = self.get_timestamp_seconds()
        token_str = api_token.get_token_str()
        
        with self.r.pipeline() as pipe:
            while True:
                if self.is_timeout(start_timestamp):
                    raise ValueError('Operation timed out.')
                
                try:
                    # Watch the token for changes
                    pipe.watch(token_str)
                    
                    if (int(pipe.exists(token_str)) == 1):
                        raise ValueError('Token already exists.')
                    
                    # Start the transaction
                    pipe.multi()
                    pipe.json().set(token_str, ROOT_PATH, api_token.data.__dict__)
                    
                    # Execute the transaction
                    res = pipe.execute()
                    print("Token created:", res)
                    break
                    
                except redis.WatchError:
                    # If a WatchError is raised, it means that the watched key was modified
                    # by another client before the transaction could be completed. In this
                    # case, retry the operation.
                    continue
        

    def delete_token(self, token: str):
        """
        Delete a token from Redis.
        
        Args:
            token (str): The token to delete.
        """
        # 1: deleted existing, 0: does not exist
        result = self.r.delete(TokenHandler.format(token))
        if result == 0:
            raise ValueError('Token does not exist.')
        
        print("Token deleted, status:", result)
        
        
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


    def use_token(self, token: str) -> ApiToken:
        """
        Use a token in Redis.
        
        Args:
            token (str): The token to use.
        """
        token_str = TokenHandler.format(token)
        start_timestamp = self.get_timestamp_seconds()
        
        with self.r.pipeline() as pipe:
            while True:
                try:
                    if self.is_timeout(start_timestamp):
                        raise ValueError('Operation timed out.')
                    
                    # Watch the token for changes
                    pipe.watch(token_str)
                    
                    if (int(pipe.exists(token_str)) == 0):
                        raise ValueError('Token does not exist.')

                    # Fetch current values
                    token_data = pipe.json().get(token_str)
                    
                    if not token_data:
                        raise ValueError('Token not found.')

                    # Start the transaction
                    pipe.multi()
                    
                    if token_data['access_count'] + 1 >= token_data['access_limit']:
                        pipe.delete(token_str)
                    else:
                        # increment access count
                        pipe.json().numincrby(token_str, 'access_count', 1)

                    
                    # Execute the transaction
                    res = pipe.execute()
                    print(res)
                    
                    # Check if the transaction was successful
                    # !TODO: Implement better error handling
                    if not (len(res) == 1):
                        raise ValueError('Transaction failed.')
                    
                    return ApiToken(token, ApiTokenData(**token_data))
                    
                except redis.WatchError:
                    # If a WatchError is raised, it means that the watched key was modified
                    # by another client before the transaction could be completed. In this
                    # case, retry the operation.
                    continue
    
    