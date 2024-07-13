class ServerError(Exception):
    """
    Base class for Server errors.

    Args:
        message (str): The error message
        status_code (int): The status code of the error
        prefix (str): The prefix of the error message
    """

    def __init__(self, message, status_code=500, prefix="Internal Error: "):
        self.message = message
        self.message_with_prefix = prefix + message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(ServerError):
    """
    Class for authentication errors, a subclass of ServerError.
    status_code is 401.

    Args:
        message (str): The error message
    """

    def __init__(self, message):
        super().__init__(message, 401, "Unauthorized: ")


class ForbiddenError(ServerError):
    """
    Class for forbidden errors, a subclass of ServerError.
    status_code is 403.

    Args:
        message (str): The error message
    """

    def __init__(self, message):
        super().__init__(message, 403, "Permission Denied: ")


class NotFoundError(ServerError):
    """
    Class for not found errors, a subclass of ServerError.
    status_code is 404.

    Args:
        message (str): The error message
    """

    def __init__(self, message):
        super().__init__(message, 404, "Not Found: ")
