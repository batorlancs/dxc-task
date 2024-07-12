import sys
import redis_database
from api_token import ApiToken


def run_command(arg1: str = None, arg2: str = None):
    # connect to the Redis database
    db = redis_database.RedisDatabase()
    
    args = []
    if arg1: args.append(arg1)
    if arg2: args.append(arg2)
    
    if len(args) < 1:
        print("Invalid argument.")
        
    elif args[0] == 'create':
        if len(args) < 2:
            print("Invalid argument. Did you mean: create <token>")
        elif args[1]:
            db.create_token(ApiToken(args[1]))
        
    elif args[0] == 'delete':
        if len(args) < 2:
            print("Invalid argument. Did you mean: delete <token>")
        elif args[1]:
            db.delete_token(args[1])
            
    elif args[0] == 'use':
        if len(args) < 2:
            print("Invalid argument. Did you mean: use <token>")
        elif args[1]:
            token = db.use_token(args[1], "")
            print("----------------------------")
            print(token.get_token_str())
            print(token.get_mapping_dict())
            print("----------------------------")
            
    else:
        print("Invalid argument. Try: create, delete, or use.")
        

args = sys.argv[1:]
run_command(*args)
