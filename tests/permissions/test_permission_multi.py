import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_multiple_permissions(permissions: list[str]) -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, permissions))
    await db.create_token(token)
    return token


async def delete_token(token: ApiToken):
    await db.delete_token(token.token)

    
@pytest.mark.asyncio(scope="class")
class TestPermissionMulti:
    
    PERMISSIONS_API1_API2 = ["api1", "api2"]
    PERMISSIONS_API1_API3 = ["api1", "api3"]
    PERMISSIONS_API2_API3 = ["api2", "api3"]
    PERMISSIONS_API1_API2_API3 = ["api1", "api2", "api3"]
    PERMISSIONS_API1_NON_EXISTENT = ["api1", "this/api/should/not/exist"]
    PERMISSIONS_API2_API3_NON_EXISTENT = ["api2", "api3", "this/api/should/not/exist"]
    PERMISSIONS_NON_EXISTENT_NON_EXISTENT = ["first/api/should/not/exist", "second/api/should/not/exist"]
    
    @pytest.mark.parametrize("api_url, permissions, expected_status_code, expected_response", [
        (API1_URL, PERMISSIONS_API1_API2, 200, "API1"),
        (API2_URL, PERMISSIONS_API1_API2, 200, "API2"),
        (API3_URL, PERMISSIONS_API1_API2, 403, "Permission Denied"),
        
        (API1_URL, PERMISSIONS_API1_API3, 200, "API1"),
        (API2_URL, PERMISSIONS_API1_API3, 403, "Permission Denied"),
        (API3_URL, PERMISSIONS_API1_API3, 200, "API3"),
        
        (API1_URL, PERMISSIONS_API2_API3, 403, "Permission Denied"),
        (API2_URL, PERMISSIONS_API2_API3, 200, "API2"),
        (API3_URL, PERMISSIONS_API2_API3, 200, "API3"),
        
        (API1_URL, PERMISSIONS_API1_API2_API3, 200, "API1"),
        (API2_URL, PERMISSIONS_API1_API2_API3, 200, "API2"),
        (API3_URL, PERMISSIONS_API1_API2_API3, 200, "API3"),
        
        (API1_URL, PERMISSIONS_API1_NON_EXISTENT, 200, "API1"),
        (API2_URL, PERMISSIONS_API1_NON_EXISTENT, 403, "Permission Denied"),
        (API3_URL, PERMISSIONS_API1_NON_EXISTENT, 403, "Permission Denied"),
        
        (API1_URL, PERMISSIONS_API2_API3_NON_EXISTENT, 403, "Permission Denied"),
        (API2_URL, PERMISSIONS_API2_API3_NON_EXISTENT, 200, "API2"),
        (API3_URL, PERMISSIONS_API2_API3_NON_EXISTENT, 200, "API3"),
        
        (API1_URL, PERMISSIONS_NON_EXISTENT_NON_EXISTENT, 403, "Permission Denied"),
        (API2_URL, PERMISSIONS_NON_EXISTENT_NON_EXISTENT, 403, "Permission Denied"),
        (API3_URL, PERMISSIONS_NON_EXISTENT_NON_EXISTENT, 403, "Permission Denied"),
    ])
    async def test_permission_multi_access_to_apis(self, api_url, permissions, expected_status_code, expected_response):
        token = await create_token_with_multiple_permissions(permissions)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
            