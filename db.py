import redis
from typing import Optional
from api_token import ApiToken, ApiTokenData, TokenHandler
from redis import Redis


# Connect to Redis
r = Redis(host='localhost', port=6379, db=0, decode_responses=True)


def create_token(api_token: Optional[ApiToken] = ApiToken()):
    """
    Create a token in Redis with the given access count and limit.
    
    Args:
        token (str): The token to create.
        access_count (int): The number of times the token has been accessed.
        access_limit (int): The maximum number of times the token can be accessed.
    """
    num_fields_added = r.hset(
        api_token.get_token_str(),
        mapping=api_token.get_mapping_dict()
    )
    
    if num_fields_added == 0:
        raise ValueError('Token already exists.')


def delete_token(token: str):
    """
    Delete a token from Redis.
    
    Args:
        token (str): The token to delete.
    """
    result = r.delete(TokenHandler.format(token))
    if result == 0:
        raise ValueError('Token does not exist.')
    
    
def token_exists(token: str) -> bool:
    """
    Check if a token exists in Redis.
    
    Args:
        token (str): The token to check.
        
    Returns:
        bool: True if the token exists, False otherwise.
    """
    num_exists = r.exists(TokenHandler.format(token))
    if num_exists == 0:
        return False
    
    return True


def use_token(token: str) -> ApiToken:
    """
    Use a token in Redis.
    
    Args:
        token (str): The token to use.
    """
    token_str = TokenHandler.format(token)
    start_timestamp_seconds = r.time()[0]
    max_time_seconds = 15
    
    with r.pipeline() as pipe:
        while True:
            try:
                if r.time()[0] - start_timestamp_seconds > max_time_seconds:
                    raise ValueError('Operation timed out.')
                
                # Watch the token for changes
                pipe.watch(token_str)
                
                if (int(pipe.exists(token_str)) == 0):
                    raise ValueError('Token does not exist.')

                # Fetch current values
                access_count = int(pipe.hget(token_str, 'access_count'))
                access_limit = int(pipe.hget(token_str, 'access_limit'))

                # Start the transaction
                pipe.multi()
                pipe.hincrby(token_str, 'access_count', 1)
                
                if access_count + 1 >= access_limit:
                    pipe.delete(token_str)
                
                pipe.hgetall(token_str)
                
                # Execute the transaction
                res = pipe.execute()
                print(res)
                
                # Check if the transaction was successful
                # !TODO: Implement better error handling
                if not (len(res) == 2 or len(res) == 3):
                    raise ValueError('Transaction failed.')
                
                updated_token = res[-1]
                if not updated_token:
                    raise ValueError('Token not found.')
                
                return ApiToken(token, ApiTokenData(**updated_token))
                
            except redis.WatchError:
                # If a WatchError is raised, it means that the watched key was modified
                # by another client before the transaction could be completed. In this
                # case, retry the operation.
                continue
    
    