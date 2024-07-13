import pytest
import requests
import uuid
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_single_permission(permission: str) -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, [permission]))
    await db.create_token(token)
    return token


@pytest.mark.asyncio(scope="class")
class TestTokenWithLeadingSlashSingle:
    
    # permission: "/" (home)
    
    async def test_home_permission_cant_access_api1(self):
        token = await create_token_with_single_permission("/")
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_home_permission_cant_access_api2(self):
        token = await create_token_with_single_permission("/")
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_home_permission_cant_access_api3(self):
        token = await create_token_with_single_permission("/")
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    # permission: "/api1"
    
    async def test_api1_permission_can_access_api1(self):
        token = await create_token_with_single_permission("/api1")
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 200
        assert resp.text == "API1"
        
    async def test_api1_permission_cant_access_api2(self):
        token = await create_token_with_single_permission("/api1")
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_api1_permission_cant_access_api3(self):
        token = await create_token_with_single_permission("/api1")
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    # permission: "/api2"

    async def test_api2_permission_cant_access_api1(self):
        token = await create_token_with_single_permission("/api2")
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_api2_permission_can_access_api2(self):
        token = await create_token_with_single_permission("/api2")
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 200
        assert resp.text == "API2"
        
    async def test_api2_permission_cant_access_api3(self):
        token = await create_token_with_single_permission("/api2")
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    # permission: "/api3"
    
    async def test_api3_permission_cant_access_api1(self):
        token = await create_token_with_single_permission("/api3")
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_api3_permission_cant_access_api2(self):
        token = await create_token_with_single_permission("/api3")
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_api3_permission_can_access_api3(self):
        token = await create_token_with_single_permission("/api3")
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 200
        assert resp.text == "API3"
        
    # permission: "/does-not-exist"
    
    async def test_non_existent_permission_cant_access_api1(self):
        token = await create_token_with_single_permission("/does-not-exist")
        resp = requests.get(API1_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_non_existent_permission_cant_access_api2(self):
        token = await create_token_with_single_permission("/does-not-exist")
        resp = requests.get(API2_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
        
    async def test_non_existent_permission_cant_access_api3(self):
        token = await create_token_with_single_permission("/does-not-exist")
        resp = requests.get(API3_URL, headers={
            "token": token.token
        })
        assert resp.status_code == 403
        assert resp.text.startswith("Permission Denied")
