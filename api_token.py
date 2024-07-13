import uuid
from typing import Optional


class TokenHandler:
    @staticmethod
    def format(token: str):
        return f"token:{token}"

    @staticmethod
    def parse(token: str):
        return token.split(":")[1]
    
    @staticmethod
    def detect(token: str):
        return token.startswith("token:") and len(token) > 6


class ApiTokenData:
    def __init__(
        self,
        access_count: Optional[int] = None,
        access_limit: Optional[int] = None,
        scopes: Optional[list] = [],
    ):
        self.access_count = access_count or 0
        self.access_limit = access_limit or 40
        self.scopes = scopes or []
    
    def validate(self) -> bool:
        return not (self.access_count < 0 or self.access_limit < 0 or self.access_count >= self.access_limit)
    
    @classmethod
    def from_dict(cls, data_dict: dict = None):
        data_dict = data_dict or {}
        return cls(
            access_count=data_dict.get('access_count'),
            access_limit=data_dict.get('access_limit'),
            scopes=data_dict.get('scopes')
        )


class ApiToken:
    def __init__(
        self,
        token: Optional[str] = None,
        data: Optional[ApiTokenData] = None,
    ):
        self.token = self.handle_token(token)
        self.data = data or ApiTokenData()

    def handle_token(self, token: str) -> str:
        token = token or uuid.uuid4().hex
        if TokenHandler.detect(token):
            return TokenHandler.parse(token)
        return token

    def get_token_str(self) -> str:
        return TokenHandler.format(self.token)
    
    def validate(self) -> bool:
        data_valid = self.data.validate()
        valid = True # implement if needed
        return data_valid and valid

    @classmethod
    def from_dict(cls, token_dict: dict = None):
        token_dict = token_dict or {}
        return cls(
            token=token_dict.get('token'),
            data=ApiTokenData.from_dict(token_dict.get('data'))
        )
