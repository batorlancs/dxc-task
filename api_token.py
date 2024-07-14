import uuid
from typing import Optional


class TokenHandler:
    """
    Handle the token database formatting.
    Database format: token:<token>
    ApiToken format: <token>
    """
    @staticmethod
    def format(token: str):
        """Format the token to the database format."""
        return f"token:{token}"

    @staticmethod
    def parse(token: str):
        """Parse the token from the database format."""
        return token.split(":")[1]

    @staticmethod
    def detect(token: str):
        """Detect if the token is in the database format."""
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
        """
        Validate the token data.

        Returns:
            bool: True if the token data is valid, False otherwise.
        """
        return not (self.access_count < 0 or self.access_limit < 0 or self.access_count >= self.access_limit)

    @classmethod
    def from_dict(cls, data_dict: dict = None):
        data_dict = data_dict or {}
        return cls(
            access_count=data_dict.get('access_count'),
            access_limit=data_dict.get('access_limit'),
            scopes=data_dict.get('scopes')
        )

    def __str__(self):
        return f"access_count: {self.access_count}, access_limit: {self.access_limit}, scopes: {self.scopes}"


class ApiToken:
    def __init__(
        self,
        token: Optional[str] = None,
        data: Optional[ApiTokenData] = None,
    ):
        self.token = self.handle_token(token)
        self.data = data or ApiTokenData()

    def handle_token(self, token: str) -> str:
        """
        Be able to handle the token in different formats.

        Args:
            token (str): The token to handle.

        Returns:
            str: The token in the correct format to store.
        """
        token = token or uuid.uuid4().hex
        if TokenHandler.detect(token):
            return TokenHandler.parse(token)
        return token

    def get_token_str(self) -> str:
        """Get the token in the database format (token:<token>)."""
        return TokenHandler.format(self.token)

    def validate(self) -> bool:
        """
        Validate the token.

        Returns:
            bool: True if the token is valid, False otherwise.
        """
        data_valid = self.data.validate()
        valid = True  # implement if needed
        return data_valid and valid

    @classmethod
    def from_dict(cls, token_dict: dict = None):
        token_dict = token_dict or {}
        return cls(
            token=token_dict.get('token'),
            data=ApiTokenData.from_dict(token_dict.get('data'))
        )

    def __str__(self):
        return f"token: {self.token}, data: {self.data}"
