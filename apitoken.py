import uuid
from redis_om import (Field, JsonModel)
from pydantic import NonNegativeInt, PositiveInt


class ApiToken(JsonModel):
    token: str = Field(index=True, default=lambda: uuid.uuid4().hex, primary_key=True)
    access_count: NonNegativeInt = Field(index=True, default=0)
    access_limit: PositiveInt = Field(index=True, default=40)
