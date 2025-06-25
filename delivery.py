import os
import json
from uuid import uuid4

def deliver_account():
    folder = 'files'
    for file in os.listdir(folder):
        if file.endswith('.txt'):
            path = os.path.join(folder, file)
            os.remove(path)
            return path
    return None

def save_pending_account(user_id, data):
    acc_id = str(uuid4())[:8]
    try:
        with open("database/pending.json", "r") as f:
            pending = json.load(f)
    except:
        pending = {}
    pending[acc_id] = {"user_id": user_id, "data": data}
    with open("database/pending.json", "w") as f:
        json.dump(pending, f)
    return acc_id

def list_pending_accounts():
    try:
        with open("database/pending.json", "r") as f:
            return json.load(f)
    except:
        return {}

def approve_account(acc_id):
    with open("database/pending.json", "r") as f:
        pending = json.load(f)
    data = pending.pop(acc_id, None)
    if data:
        with open(f"files/{acc_id}.txt", "w") as f:
            f.write(data["data"])
    with open("database/pending.json", "w") as f:
        json.dump(pending, f)

def reject_account(acc_id):
    with open("database/pending.json", "r") as f:
        pending = json.load(f)
    pending.pop(acc_id, None)
    with open("database/pending.json", "w") as f:
        json.dump(pending, f)