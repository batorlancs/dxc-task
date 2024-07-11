import uuid
from typing import Optional

class TokenHandler:
    @staticmethod
    def format(token: str):
        return f"token:{token}"
    
    @staticmethod
    def parse(token: str):
        return token.split(":")[1]
    

class ApiTokenData:
    def __init__(
        self,
        access_count: Optional[int] = 0,
        access_limit: Optional[int] = 40,
    ):
        self.access_count = access_count
        self.access_limit = access_limit
        
    def validate(self) -> str:
        # !TODO: Implement validation
        return ""


class ApiToken:
    def __init__(
        self,
        token: Optional[str] = uuid.uuid4().hex,
        data: Optional[ApiTokenData] = ApiTokenData(),
    ):
        self.token = token
        self.data = data
        
        validation_error = self.validate()
        if validation_error:
            raise ValueError(validation_error)
    
    def get_token_str(self):
        return TokenHandler.format(self.token)
    
    def get_mapping_dict(self):
        return self.data.__dict__
    
    def validate(self) -> str:
        # !TODO: Implement validation
        return ""