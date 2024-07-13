import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_no_permissions() -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, []))
    await db.create_token(token)
    return token
    

@pytest.fixture(scope="class", autouse=True)
async def token():
    token = await create_token_with_no_permissions()
    yield token


@pytest.mark.asyncio(scope="class")
class TestTokenWithNoPermissions:
    async def test_cant_access_to_api1(self, token: ApiToken):
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_cant_access_to_api2(self, token: ApiToken):
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_cant_access_to_api3(self, token: ApiToken):
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")