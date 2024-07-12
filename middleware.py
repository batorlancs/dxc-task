from redis_database import RedisDatabase
from socketify import App, MiddlewareRouter, Response, Request
from errors import DatabaseError, AuthError, NotFoundError


class AuthMiddlewareRouter(MiddlewareRouter):
    def __init__(self, app: App, db: RedisDatabase):
        super().__init__(app, self.auth)
        self.app = app
        self.db = db
        

    def auth(self, res: Response, req: Request, data=None):
        header_token = req.get_header("token")
        if not header_token:
            res.write_status(401).end("No token provided.")
            return False
            
        try:
            return self.db.use_token(req.get_header("token"), req.get_url())
        
        except DatabaseError as e:
            res.write_status(e.status_code).end(e.message)
            return False # stop the request from being processed further