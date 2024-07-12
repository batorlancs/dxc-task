import sys
import redis_database
import asyncio
from api_token import ApiToken, ApiTokenData


async def run_command(arg1: str = None, arg2: str = None):
    # connect to the Redis database
    db = redis_database.RedisDatabase()

    args = []
    if arg1:
        args.append(arg1)
    if arg2:
        args.append(arg2)

    if len(args) < 1:
        print("Invalid argument.")

    elif args[0] == 'create':
        if len(args) < 2:
            print("Invalid argument. Did you mean: create <token>")
        elif args[1]:
            await db.create_token(
                ApiToken(args[1], ApiTokenData(
                    access_limit=5,
                    access_count=2,
                    scopes=["*"]
                ))
            )
            print("Token created successfully.")

    elif args[0] == 'delete':
        if len(args) < 2:
            print("Invalid argument. Did you mean: delete <token>")
        elif args[1]:
            await db.delete_token(args[1])

    elif args[0] == 'use':
        if len(args) < 2:
            print("Invalid argument. Did you mean: use <token>")
        elif args[1]:
            token = await db.get_and_use_token(args[1], "/api1")
            print("----------------------------")
            print(token.get_token_str())
            print(token.data.__dict__)
            print("----------------------------")

    else:
        print("Invalid argument. Try: create, delete, or use.")


args = sys.argv[1:]
asyncio.run(run_command(*args))
