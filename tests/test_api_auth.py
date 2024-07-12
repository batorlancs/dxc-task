# import pytest
# import requests
# import uuid
# from tests.config import API1_URL, API2_URL, API3_URL
# from redis_db import db
# from api_token import ApiToken, ApiTokenData


# # async def create_token_to_use() -> ApiToken:
# #     token = ApiToken(data=ApiTokenData(0, 3, ["api1", "api2", "api3"]))
# #     await db.create_token(token)
# #     return token

# # @pytest.fixture(scope="class", autouse=True)
# # async def token():
# #     token = await create_token_to_use()
# #     yield token
# #     # cleanup after


# class TestApiAuth:
#     async def test_non_existent_token(self):
#         resp = requests.get(API1_URL, headers={
#             "token": "this-token-does-not-exist" + uuid.uuid4().hex
#         })
#         assert resp.status_code == 401
#         assert resp.text == "Token is not valid."
        
#     async def test_permission_access_with_all_permissions(self):
#         token = await db.create_token(
#             ApiToken(
#                 data=ApiTokenData(
#                     access_limit=1,
#                     scopes=["*"]
#                 )
#             )
#         )
        
#         resp = requests.get(API1_URL, headers={
#             "token": token.token
#         })
#         assert resp.status_code == 200
#         assert resp.text == "API1"
 