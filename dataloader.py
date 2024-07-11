import json
import db
import sys


def load_single_token():
    with open("data/single.json", encoding="utf-8") as f:
        token = json.load(f)
        
    response = db.create_token(
        token=token.get("token"),
        access_count=token.get("access_count"),
        access_limit=token.get("access_limit"),
    )
    
    if response:
        print("Token created successfully:", response)
    else:
        print("Failed to create token")


arg1 = sys.argv[1]        

if arg1 == "single":
    load_single_token()
else:
    print("Invalid argument")