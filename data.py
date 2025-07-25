from pathlib import Path
import json
from datetime import datetime

DATA_FILE = Path("social_data.json")

DEFAULT_DATA = {
    "users": [],
    "brands": [],
    "posts": [],
    "media": []
}

def load_data():
    if DATA_FILE.exists():
        with DATA_FILE.open() as f:
            return json.load(f)
    return DEFAULT_DATA.copy()

def save_data(data):
    with DATA_FILE.open('w') as f:
        json.dump(data, f, indent=2)

def create_user(username, password_hash):
    data = load_data()
    if any(u['username'] == username for u in data['users']):
        return False
    data['users'].append({"username": username, "password": password_hash})
    save_data(data)
    return True

def verify_user(username, password_hash):
    data = load_data()
    return any(u['username'] == username and u['password'] == password_hash for u in data['users'])


def add_brand(brand_name):
    data = load_data()
    if any(b['name'] == brand_name for b in data['brands']):
        return False
    data['brands'].append({"name": brand_name, "accounts": {}})
    save_data(data)
    return True

def add_account(brand_name, platform, username):
    data = load_data()
    for b in data['brands']:
        if b['name'] == brand_name:
            b['accounts'].setdefault(platform, [])
            if username not in b['accounts'][platform]:
                b['accounts'][platform].append(username)
                save_data(data)
                return True
            return False
    return False

def schedule_post(brand_name, platform, message, post_time=None):
    data = load_data()
    data['posts'].append({
        "brand": brand_name,
        "platform": platform,
        "message": message,
        "time": post_time,
        "posted": False
    })
    save_data(data)


def list_posts():
    data = load_data()
    return data['posts']


def mark_posted(post_index):
    data = load_data()
    if 0 <= post_index < len(data['posts']):
        data['posts'][post_index]['posted'] = True
        save_data(data)
        return True
    return False

