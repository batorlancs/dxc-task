import sys
import redis_db
import asyncio
from api_token import ApiToken, ApiTokenData
from redis_db import db


async def run_command(args: list[str]):
    # connect to the Redis database

    if len(args) < 1:
        raise RuntimeError("No command provided. Try: create, delete, or use.")

    command, *remaining_args = args

    if command == 'create':
        if len(remaining_args) < 1:
            print("Invalid syntax. Did you mean: create <token>")
            return

        await db.create_token(
            ApiToken(args[1], ApiTokenData(
                access_limit=5,
                access_count=2,
                scopes=["*"]
            ))
        )
        print("Token created successfully.")

    elif command == "delete":
        if len(remaining_args) < 1:
            print("Invalid syntax. Did you mean: delete <token>")
            return

        await db.delete_token(args[1])
        print("Token deleted successfully.")

    elif command == 'use':
        if len(remaining_args) < 1:
            print("Invalid syntax. Did you mean: use <token>")
            return

        token = await db.get_and_use_token(args[1], "/api1")
        print("----------------------------")
        print(token.get_token_str())
        print(token.data.__dict__)
        print("----------------------------")

    else:
        print("Invalid command. Try: create, delete, or use.")


args = sys.argv[1:]
asyncio.run(run_command(args))
