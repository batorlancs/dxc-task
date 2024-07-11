import db
import sys
from api_token import ApiToken

args = sys.argv[1:]

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
        db.use_token(args[1])
        
else:
    print("Invalid argument. Try: create, delete, or use.")