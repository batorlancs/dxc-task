from socketify import App

def make_app(app: App):
    app.get("/", lambda res, req: res.end("Hello World!"))

if __name__ == "__main__":
    app = App()
    make_app(app)
    app.listen(3000, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))
    app.run()