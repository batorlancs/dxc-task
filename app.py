from loguru import logger
from redis_database import RedisDatabase
from socketify import App
from middleware import AuthMiddlewareRouter


def api_1(res, req, data=None):
    res.write_status(200).end("API1")


def api_2(res, req, data=None):
    res.write_status(200).end("API2")


def api_3(res, req, data=None):
    res.write_status(200).end("API3")


db = RedisDatabase(check_connection=True) # connect to the redis database

app = App()
logger.info("Initiating the server...")

# middleware
auth_router = AuthMiddlewareRouter(app, db)
auth_router.get("/api1", api_1)
auth_router.get("/api2", api_2)
auth_router.get("/api3", api_3)

# handle endpoints not found
app.any("/*", lambda res, req, data=None: res.write_status(404).end("Not found."))


@app.on_error
def on_error(error, res, req):
    # here you can log properly the error and do a pretty response to your clients
    logger.error(f"Some internal error occurred: {error}")
    # response and request can be None if the error is in an async function
    if res is not None:
        # if response exists try to send something
        res.write_status(500).end("Internal server error")


# start the server
app.listen(3000, lambda config: logger.success(f"Listening on port http://localhost:{config.port}"))
app.run()
