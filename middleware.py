from loguru import logger
from db.db_manager import db
from socketify import App, MiddlewareRouter, Response, Request
from errors import ServerError, AuthenticationError, ForbiddenError
from db.errors import DatabaseError, TokenNotValidError, TokenPermissionError


class AuthMiddlewareRouter(MiddlewareRouter):
    """
    Middleware class for authentication.

    This class is responsible for checking the headers and token in the request.
    """

    def __init__(self, app: App):
        super().__init__(app, self.auth)
        self.app = app

    def check_headers(self, headers: dict):
        """
        Check if the headers contain the correct parameters.

        Args:
            headers (dict): The headers of the request.

        Raises:
            AuthenticationError: If the headers do not contain the correct parameters.
        """
        if "token" not in headers:
            raise AuthenticationError("Please provide a token in the headers.")

    async def auth(self, res: Response, req: Request, data=None):
        headers = req.get_headers()
        url = req.get_url()
        logger.info(f"---> url: {url}, token: {headers['token'] or 'None'}")

        try:
            logger.debug(f"Checking headers...")
            self.check_headers(headers)
            logger.debug(f"Checking token: {headers['token']}")
            response = db.get_and_use_token(headers["token"], url)
            logger.success(f"Authenticated, with token: {response}")
            return response

        except DatabaseError as e:
            # errors related to the database
            error_mapping = {
                TokenNotValidError: AuthenticationError(e.message),
                TokenPermissionError: ForbiddenError(e.message)
            }
            error_response = error_mapping.get(type(e), ServerError(e.message))

            logger.error(f"Responded: Error {error_response.status_code}: {error_response.message}")
            res.write_status(error_response.status_code).end(error_response.message_with_prefix)
            return False  # stop the request from being processed further

        except ServerError as e:
            # errors related to the server
            logger.error(f"Responded: Error {e.status_code}: {e.message}")
            res.write_status(e.status_code).end(e.message_with_prefix)
            return False
