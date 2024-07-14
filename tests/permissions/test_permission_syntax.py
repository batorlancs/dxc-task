import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_multi_permissions(permissions: list[str]) -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, permissions))
    db.create_token(token)
    return token


async def delete_token(token: ApiToken):
    db.delete_token(token.token)


@pytest.mark.asyncio(scope="class")
class TestPermissionSyntax:

    # - "*" access to all endpoints and home
    # - "" access to just home (or "/")
    # - "api/" access to all endpoints in the api but not api itself (or "/api/")
    # - "api*" access to all endpoints in the api including api itself (or "/api*")
    # - "api" access to the specific endpoint (or "/api")

    @pytest.mark.parametrize("api_url, permissions, expected_status_code, expected_response", [
        # no permissions
        (API1_URL, [], 403, "Permission Denied"),
        (API2_URL, [], 403, "Permission Denied"),
        (API3_URL, [], 403, "Permission Denied"),
        # all permissions
        (API1_URL, ["*"], 200, "API1"),
        (API2_URL, ["*"], 200, "API2"),
        (API3_URL, ["*"], 200, "API3"),
        # home
        (API1_URL, [""], 403, "Permission Denied"),
        (API2_URL, [""], 403, "Permission Denied"),
        (API3_URL, [""], 403, "Permission Denied"),
        # also counts as home
        (API1_URL, ["/"], 403, "Permission Denied"),
        (API2_URL, ["/"], 403, "Permission Denied"),
        (API3_URL, ["/"], 403, "Permission Denied"),
        # everything in api1, api2, api3 but not api1, api2, api3
        (API1_URL, ["api1/"], 403, "Permission Denied"),
        (API2_URL, ["api2/"], 403, "Permission Denied"),
        (API3_URL, ["api3/"], 403, "Permission Denied"),
        # everything in api1, api2, api3 including api1, api2, api3
        (API1_URL, ["api1*"], 200, "API1"),
        (API2_URL, ["api2*"], 200, "API2"),
        (API3_URL, ["api3*"], 200, "API3"),
        # everything in api (api1, api2, api3 are not in api) including api
        (API1_URL, ["api*"], 403, "Permission Denied"),
        (API2_URL, ["api*"], 403, "Permission Denied"),
        (API3_URL, ["api*"], 403, "Permission Denied"),
        # everything in api (api1, api2, api3 are not in api) but not api
        (API1_URL, ["api/"], 403, "Permission Denied"),
        (API2_URL, ["api/"], 403, "Permission Denied"),
        (API3_URL, ["api/"], 403, "Permission Denied"),
    ])
    async def test_permission_multi_access_to_apis(self, api_url, permissions, expected_status_code, expected_response):
        token = await create_token_with_multi_permissions(permissions)
        resp = requests.get(api_url, headers={
            "token": token.token
        })
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
