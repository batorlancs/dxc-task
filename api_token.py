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
        scopes: Optional[list] = [],
    ):
        self.access_count = access_count
        self.access_limit = access_limit
        self.scopes = scopes


class ApiToken:
    def __init__(
        self,
        token: Optional[str] = None,
        data: Optional[ApiTokenData] = ApiTokenData(),
    ):
        self.token = token or uuid.uuid4().hex
        self.data = data

    def get_token_str(self):
        return TokenHandler.format(self.token)

    def __dict__(self):
        return {
            "token": self.token,
            "data": self.data.__dict__
        }
