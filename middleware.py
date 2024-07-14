from loguru import logger
from db.db_manager import db
from socketify import App, MiddlewareRouter, Response, Request
from errors import ServerError, AuthenticationError, NotFoundError


class AuthMiddlewareRouter(MiddlewareRouter):
    def __init__(self, app: App):
        super().__init__(app, self.auth)
        self.app = app

    def check_headers(self, headers: dict):
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

        except ServerError as e:
            logger.error(f"Error {e.status_code}: {e.message}")
            res.write_status(e.status_code).end(e.message_with_prefix)
            return False  # stop the request from being processed further
