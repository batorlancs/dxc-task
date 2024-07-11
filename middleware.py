from redis_database import RedisDatabase
from socketify import App, MiddlewareRouter


class AuthMiddlewareRouter(MiddlewareRouter):
    def __init__(self, app: App, db: RedisDatabase):
        super().__init__(app, self.auth)
        self.app = app
        self.db = db
        

    def auth(self, res, req, data=None):
        token = self.get_token(req.get_header("token"))
        if not token:
            res.write_status(403).end("token not valid")
            # stop the execution of the next middlewares
            return False

        # returns extra data
        return token
    
    
    def get_token(self, token: str):
        if token:
            api_token = self.db.use_token(token)
            return api_token
        return None