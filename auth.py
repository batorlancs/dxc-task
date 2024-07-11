import db


async def get_token(token):
    if token:
        api_token = db.use_token(token)
        return api_token
    return None


async def auth(res, req, data=None):
    token = await get_token(req.get_header("token"))
    if not token:
        res.write_status(403).end("token not valid")
        # stop the execution of the next middlewares
        return False

    # returns extra data
    return token