# assets_manager.py
import json, os

ASSETS_FILE = "assets_data.json"

def load_assets():
    if not os.path.exists(ASSETS_FILE):
        with open(ASSETS_FILE, "w") as f:
            json.dump({}, f)
    with open(ASSETS_FILE, "r") as f:
        return json.load(f)

def save_assets(data):
    with open(ASSETS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_asset(asset_id, asset_type, name, path, tags=None):
    data = load_assets()
    if tags is None:
        tags = []
    data[asset_id] = {"type": asset_type, "name": name, "path": path, "tags": tags}
    save_assets(data)
    print(f"[ASSETS] Added asset '{name}' ({asset_type})")

def get_asset(asset_id):
    return load_assets().get(asset_id)

def list_assets():
    data = load_assets()
    for asset_id, info in data.items():
        print(f"{asset_id}: {info['name']} ({info['type']}) - Tags: {info['tags']}")