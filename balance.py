import json

def get_balance(user_id):
    try:
        with open('database/users.json', 'r') as f:
            users = json.load(f)
        return users.get(user_id, 0)
    except:
        return 0