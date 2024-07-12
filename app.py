import sys
from loguru import logger
from redis_database import RedisDatabase
from socketify import App, Response, Request, AppListenOptions
from middleware import AuthMiddlewareRouter
from endpoints import setup_auth_endpoints


# Connect to the redis database
db = RedisDatabase(check_connection=True)

logger.info("Initiating the server...")
app = App()


@app.on_error
def on_error(error, res: Response, req: Request):
    """
    Handle all unexpected errors that occur in the server.
    """
    logger.error(f"An unexpected error occurred: {error}")
    # response and request can be None if the error is in an async function
    if res is not None:
        res.write_status(500).end("Internal Server Error")


# setup the middleware auth and endpoints
auth_router = AuthMiddlewareRouter(app, db)
setup_auth_endpoints(auth_router) # create the endpoints
    

# handle 404 errors
app.any("/*", lambda res, req: res.write_status(404).end("Not Found"))

# start the server
app.listen(
    AppListenOptions(port=3000, host="localhost"),
    lambda config: logger.success(f"Listening on port http://{config.host}:{config.port}")
)
app.run()
