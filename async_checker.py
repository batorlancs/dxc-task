import asyncio
import random
from redis_db import db
from api_token import ApiToken, ApiTokenData


async def async_checker():
    semaphore = asyncio.Semaphore(100)
    
    async def use_token(token, i):
        async with semaphore:
            # wait random small amount of time
            await asyncio.sleep((random.random()*0.2) + 2)
            print("Trying to get token, client:", i)
            return await db.get_and_use_token(token)
    
    print("Creating token..")
    token = await db.create_token(
        ApiToken(
            data=ApiTokenData(
                access_limit=500,
                scopes=["*"]
            )
        )
    )
    print(f"Token created: {token.token}")
    
    print("Getting and using token..")
    
    
    tasks = [use_token(token.token, i) for i in range(1000)]
    results = await asyncio.gather(*tasks)
    
    print("tasks completed")
    print(results)
    


if __name__ == "__main__":
    asyncio.run(async_checker())