import sys
import asyncio
import config
from redis_db import db
from loguru import logger
from socketify import App, Response, Request, AppListenOptions
from middleware import AuthMiddlewareRouter
from endpoints import setup_auth_endpoints
from environments import setup_environment_with_args, InvalidArgumentError, EnvironmentSetupError


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


async def init() -> App:
    logger.info("Initiating the server...")
    
    # check database connection
    logger.info("Checking connection to Redis...")
    is_connected = db.check_connection()
    if not is_connected:
        logger.error("Database connection failed. Exiting the server...")
        sys.exit(1)
    logger.success("Database connection successful.")
    
    
    # setup the middleware auth and endpoints
    auth_router = AuthMiddlewareRouter(app)
    setup_auth_endpoints(auth_router) # create the endpoints

    # setup the environment
    try:
        await setup_environment_with_args(sys.argv)
    except InvalidArgumentError as e:
        logger.error(e)
        logger.warning("Continuing with the default environment...")
    except EnvironmentSetupError as e:
        logger.error(e)
        logger.info("Exiting the server...")
        sys.exit(1)
    

    # handle 404 errors
    app.any("/*", lambda res, req: res.write_status(404).end("Not Found"))

    # start the server
    app.listen(
        AppListenOptions(port=3000, host="localhost"),
        lambda config: logger.success(f"Listening on port http://{config.host}:{config.port}")
    )


loop = asyncio.new_event_loop()
loop.run_until_complete(init())
app.run()