from socketify import App
from redis_om import Migrator
from endpoints import enable_endpoints

app = App()
enable_endpoints(app)
app.listen(3000, lambda config: print("Listening on port http://localhost:%d now\n" % config.port))
Migrator().run()
app.run()
