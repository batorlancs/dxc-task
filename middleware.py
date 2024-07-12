from redis_database import RedisDatabase
from socketify import App, MiddlewareRouter, Response, Request
from errors import ServerError, AuthenticationError, NotFoundError


class AuthMiddlewareRouter(MiddlewareRouter):
    def __init__(self, app: App, db: RedisDatabase):
        super().__init__(app, self.auth)
        self.app = app
        self.db = db

    def check_headers(self, headers: dict):
        if "token" not in headers:
            raise AuthenticationError("Please provide a token in the headers.")

    def auth(self, res: Response, req: Request, data=None):
        headers = req.get_headers()
        url = req.get_url()
        print("------------------------")
        print("url:", url)

        try:
            self.check_headers(headers)
            return self.db.use_token(headers["token"], url)

        except ServerError as e:
            res.write_status(e.status_code).end(e.message_with_prefix)
            return False  # stop the request from being processed further
