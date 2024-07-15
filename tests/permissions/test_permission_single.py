import pytest
import requests
from tests.config import API1_URL, API2_URL, API3_URL
from db.db_manager import db
from api_token import ApiToken, ApiTokenData


async def create_token_with_single_permission(permission: str) -> ApiToken:
    token = ApiToken(data=ApiTokenData(0, 3, [permission]))
    await db.create_token(token)
    return token


async def delete_token(token: ApiToken):
    await db.delete_token(token.token)


@pytest.mark.asyncio(scope="class")
class TestPermissionSingle:

    PERMISSION_HOME = ""
    PERMISSION_API1 = "api1"
    PERMISSION_API2 = "api2"
    PERMISSION_API3 = "api3"
    PERMISSION_NON_EXISTENT = "this/api/should/not/exist"

    @pytest.mark.parametrize("api_url, permission, expected_status_code, expected_response", [
        (API1_URL, PERMISSION_HOME, 403, "Permission Denied"),
        (API2_URL, PERMISSION_HOME, 403, "Permission Denied"),
        (API3_URL, PERMISSION_HOME, 403, "Permission Denied"),

        (API1_URL, PERMISSION_API1, 200, "API1"),
        (API2_URL, PERMISSION_API1, 403, "Permission Denied"),
        (API3_URL, PERMISSION_API1, 403, "Permission Denied"),

        (API1_URL, PERMISSION_API2, 403, "Permission Denied"),
        (API2_URL, PERMISSION_API2, 200, "API2"),
        (API3_URL, PERMISSION_API2, 403, "Permission Denied"),

        (API1_URL, PERMISSION_API3, 403, "Permission Denied"),
        (API2_URL, PERMISSION_API3, 403, "Permission Denied"),
        (API3_URL, PERMISSION_API3, 200, "API3"),

        (API1_URL, PERMISSION_NON_EXISTENT, 403, "Permission Denied"),
        (API2_URL, PERMISSION_NON_EXISTENT, 403, "Permission Denied"),
        (API3_URL, PERMISSION_NON_EXISTENT, 403, "Permission Denied")
    ])
    async def test_permission_single_access_to_apis(self, api_url, permission, expected_status_code, expected_response):
        token = await create_token_with_single_permission(permission)
        resp = requests.get(api_url, headers={"token": token.token})
        await delete_token(token)
        assert resp.status_code == expected_status_code
        if expected_status_code == 200:
            assert resp.text == expected_response
        else:
            assert resp.text.startswith(expected_response)
