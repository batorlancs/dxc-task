class DatabaseError(Exception):
    """
    Raised when an error occurs with the database.

    Args:
        message (str): The error message.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class TokenError(DatabaseError):
    """
    Raised when an error occurs with the token.

    Args:
        message (str): The error message.
    """

    def __init__(self, message):
        super().__init__(message)


class TokenNotValidError(TokenError):
    """
    Raised when the token is not valid.

    Args:
        message (str): The error message.
    """

    def __init__(self, message):
        super().__init__(message)


class TokenPermissionError(TokenError):
    """
    Raised when the token does not have the correct permissions.

    Args:
        message (str): The error message.
    """

    def __init__(self, message):
        super().__init__(message)
