import pytest
import grequests
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from db.db_manager import db
from api_token import ApiToken, ApiTokenData


async def create_token(permissions: list[str], count: int = 0, limit: int = 10) -> ApiToken:
    token = ApiToken(data=ApiTokenData(count, limit, permissions))
    await db.create_token(token)
    return token


@pytest.mark.asyncio(scope="class")
class TestLimitAsync:
    @pytest.mark.parametrize("count, limit", [
        (0, 1),
        (0, 2),
        (2, 3),
        (2, 5),
        (10, 12),
        (14, 18)
    ])
    async def test_limit_async(self, count, limit):
        token = await create_token(["api1"], count, limit)
        # use up all the api calls
        urls = [API1_URL] * (limit - count)
        reqs = [grequests.get(url, headers={"token": token.token}) for url in urls]
        responses = grequests.map(reqs)
        for resp in responses:
            assert resp.status_code == 200
            assert resp.text == "API1"

        # limit reached
        resp = requests.get(API1_URL, headers={"token": token.token})
        assert resp.status_code == 401
        assert resp.text.startswith("Unauthorized")
