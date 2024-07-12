from socketify import Response, Request, MiddlewareRouter
from simulated_api import SimulatedApi
from api_token import ApiToken


async def api1(res: Response, req: Request, token: ApiToken | None):
    response = SimulatedApi.get_api1()
    res.write_status(200).end(response)


async def api2(res: Response, req: Request, token: ApiToken | None):
    response = SimulatedApi.get_api2()
    res.write_status(200).end(response)


async def api3(res: Response, req: Request, token: ApiToken | None):
    response = SimulatedApi.get_api3()
    res.write_status(200).end(response)
    

def setup_auth_endpoints(router: MiddlewareRouter):
    router.get("/api1", api1)
    router.get("/api2", api2)
    router.get("/api3", api3)