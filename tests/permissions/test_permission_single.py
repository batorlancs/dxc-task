import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_single_permission(permission: str) -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, [permission]))
    await db.create_token(token)
    return token

async def delete_token(token: ApiToken):
    await db.delete_token(token.token)


@pytest.mark.asyncio(scope="class")
class TestPermissionSingle:
    
    # permission: "" (home)
    
    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, "", 403, "Permission Denied"),
        (API2_URL, "", 403, "Permission Denied"),
        (API3_URL, "", 403, "Permission Denied")
    ])
    async def test_home_permission_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        assert resp.text.startswith(expected_response)
        
    # permission: "api1"
    
    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, "api1", 200, "API1"),
        (API2_URL, "api1", 403, "Permission Denied"),
        (API3_URL, "api1", 403, "Permission Denied")
    ])
    async def test_api1_permission_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
        
    # permission: "api2"
    
    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, "api2", 403, "Permission Denied"),
        (API2_URL, "api2", 200, "API2"),
        (API3_URL, "api2", 403, "Permission Denied")
    ])
    async def test_api2_permission_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
        
    # permission: "api3"
    
    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, "api3", 403, "Permission Denied"),
        (API2_URL, "api3", 403, "Permission Denied"),
        (API3_URL, "api3", 200, "API3")
    ])
    async def test_api3_permission_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
        
    # permission: "api/does-not-exist"
    
    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, "api/does-not-exist", 403, "Permission Denied"),
        (API2_URL, "api/does-not-exist", 403, "Permission Denied"),
        (API3_URL, "api/does-not-exist", 403, "Permission Denied")
    ])
    async def test_non_existent_permission_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        assert resp.text.startswith(expected_response)

