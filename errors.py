class DatabaseError(Exception):
    """
    Base class for database errors.
    
    Args:
        message (str): The error message
    """
    def __init__(self, message, status_code=500, prefix="Internal Error: "):
        self.message = prefix + message
        self.status_code = status_code
        super().__init__(self.message)
        

class AuthError(DatabaseError):
    """
    Class for authentication errors, a subclass of DatabaseError.
    
    Args:
        message (str): The error message
    """
    def __init__(self, message):
        super().__init__(message, 403, "Authentication Error: ")
        
        
class NotFoundError(DatabaseError):
    """
    Class for not found errors, a subclass of DatabaseError.
    
    Args:
        message (str): The error message
    """
    def __init__(self, message):
        super().__init__(message, 404, "Not Found Error: ")