from socketify import App, MiddlewareRouter
from auth import auth


def api_1(res, req, data=None):
    res.write_status(200).end("API1")
    
def api_2(res, req, data=None):
    res.write_status(200).end("API2")
    
def api_3(res, req, data=None):
    res.write_status(200).end("API3")


app = App()
auth_router = MiddlewareRouter(app, auth)
auth_router.get("/api1", api_1)
auth_router.get("/api2", api_2)
auth_router.get("/api3", api_3)


app.listen(3000, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))
app.run()