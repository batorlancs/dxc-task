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
    await db.delete_token(token.token)


@pytest.mark.asyncio(scope="class")
class TestPermissionNone:
    
    @pytest.mark.parametrize("api_url, expected_status_code, expected_response", [
        (API1_URL, 403, "Permission Denied"),
        (API2_URL, 403, "Permission Denied"),
        (API3_URL, 403, "Permission Denied")
    ])
    async def test_cant_access_to_apis(self, token: ApiToken, api_url, expected_status_code, expected_response):
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        assert resp.status_code == expected_status_code
        assert resp.text.startswith(expected_response)