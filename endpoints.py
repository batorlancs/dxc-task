from socketify import App

def hello_world(res, req):
    res.end("Hello World!")


def enable_endpoints(app: App):
    app.get("/", hello_world)