import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token(permissions: list[str], count: int = 0, limit: int = 10) -> ApiToken:
    token = ApiToken(data=ApiTokenData(count, limit, permissions))
    await db.create_token(token)
    return token


async def delete_token(token: ApiToken):
    await db.delete_token(token.token)


def get_api_response(url: str, token: ApiToken):
    return requests.get(url, headers={
        "token": token.token
    })

    
@pytest.mark.asyncio(scope="class")
class TestLimitSync:
    @pytest.mark.parametrize("count, limit", [
        (0, 1),
        (0, 2),
        (2, 3),
        (2, 5),
        (10, 12),
        (14, 18)
    ])
    async def test_limit_sync(self, count, limit):
        token = await create_token(["api1"], count, limit)
        # use up all the api calls
        for _ in range(count, limit):
            resp = get_api_response(API1_URL, token)
            assert resp.status_code == 200
            assert resp.text == "API1"
            
        # limit reached
        resp = get_api_response(API1_URL, token)
        assert resp.status_code == 401
        assert resp.text.startswith("Unauthorized")

