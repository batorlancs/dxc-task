import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from environments import setup_test_environment
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_to_use() -> ApiToken:
    token = ApiToken(token="admin5", data=ApiTokenData(0, 3, ["api1", "api2", "api3"]))
    await db.create_token(token)
    return token
    

@pytest.fixture(scope="class", autouse=True)
async def token():
    token = await create_token_to_use()
    yield token


class TestSimpleApi:
    async def test_api1_response(self, token):
        resp = requests.get(API1_URL, headers={
            "token": "admin5"
        })
        assert resp.status_code == 200
        assert resp.text == "API1"
    
    async def test_api2_response(self, token):
        resp = requests.get(API2_URL, headers={
            "token": "admin5"
        })
        assert resp.status_code == 200
        assert resp.text == "API2"
    
    async def test_api3_response(self, token):
        resp = requests.get(API3_URL, headers={
            "token": "admin5"
        })
        assert resp.status_code == 200
        assert resp.text == "API3"