from apitoken import ApiToken
from pydantic import ValidationError
from typing import Optional


def create_token(
    token: Optional[str],
    access_count: Optional[int],
    access_limit: Optional[int],
) -> str:
    try:
        # check if token already exists
        existing_token = ApiToken.get(token)
        if existing_token:
            # !TODO: do something
            pass
        
        new_token = ApiToken(
            token=token,
            access_count=access_count,
            access_limit=access_limit,
        )
        new_token.save()
        return new_token.token
    
    except ValidationError as e:
        print("validation error when creating token: ", e)
        return None
    

def delete_token(token: str) -> bool:
    resp = ApiToken.delete(token)
    if resp == 1:
        return True # deleted existing token
    
    return False # token did not exist

