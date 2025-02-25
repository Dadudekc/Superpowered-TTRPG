import json
import os

DATA_DIR = "game_data"

# Ensure game_data directory exists
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Default JSON structures (auto-created if missing)
DEFAULT_JSONS = {
    "locations.json": {"locations": []},
    "organizations.json": {"organizations": []},
    "npcs.json": {"npcs": []},
    "arcs.json": {"arcs": []}
}

def ensure_json_exists(file_name):
    """Ensures JSON files exist; creates them with a default structure if missing."""
    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_JSONS[file_name], f, indent=4)
        print(f"✅ {file_name} was missing and has been created with a default structure.")

def load_json(file_name):
    """Loads JSON data from the specified file in the game_data directory."""
    file_path = os.path.join(DATA_DIR, file_name)
    ensure_json_exists(file_name)  # Ensure file exists before loading

    with open(file_path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON Error in {file_name}: {e}")
            return DEFAULT_JSONS[file_name]  # Return default structure in case of error

def save_json(file_name, data):
    """Saves updated JSON data to file."""
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"💾 {file_name} updated successfully.")

# ✅ LOAD FUNCTIONS
def get_locations():
    """Loads all game locations from JSON."""
    return load_json("locations.json")["locations"]

def get_organizations():
    """Loads all organizations from JSON."""
    return load_json("organizations.json")["organizations"]

def get_npcs():
    """Loads all NPCs from JSON."""
    return load_json("npcs.json")["npcs"]

def get_arcs():
    """Loads all campaign arcs from JSON."""
    return load_json("arcs.json")["arcs"]

# 🔄 UPDATE FUNCTIONS
def update_json(file_name, key, match_value, updates):
    """
    Updates an entry in a JSON file.
    
    Args:
        file_name (str): JSON file name.
        key (str): Field to match (e.g., 'id' or 'name').
        match_value (str|int): Value to match against the key.
        updates (dict): Dictionary containing fields to update.
    """
    data = load_json(file_name)
    entries = data[file_name.split(".")[0]]

    for entry in entries:
        if entry.get(key) == match_value:
            entry.update(updates)
            save_json(file_name, data)
            print(f"✅ {file_name}: Updated {key} '{match_value}' with {updates}")
            return

    print(f"❌ {key} '{match_value}' not found in {file_name}.")

# ➕ ADD ENTRY FUNCTION
def add_entry(file_name, new_entry):
    """
    Adds a new entry to a JSON file.
    
    Args:
        file_name (str): JSON file name.
        new_entry (dict): The new entry data.
    """
    data = load_json(file_name)
    key = file_name.split(".")[0]  # Extracts "locations", "npcs", etc.

    if new_entry not in data[key]:
        data[key].append(new_entry)
        save_json(file_name, data)
        print(f"✅ Added new entry to {file_name}: {new_entry['name'] if 'name' in new_entry else 'ID ' + str(new_entry.get('id'))}")
    else:
        print(f"⚠️ Entry already exists in {file_name}.")

# ❌ REMOVE ENTRY FUNCTION
def remove_entry(file_name, key, match_value):
    """
    Removes an entry from a JSON file by matching a key-value pair.
    
    Args:
        file_name (str): JSON file name.
        key (str): The field to match (e.g., 'id' or 'name').
        match_value (str|int): Value to match against the key.
    """
    data = load_json(file_name)
    key_group = file_name.split(".")[0]  # Extracts "locations", "npcs", etc.

    updated_entries = [entry for entry in data[key_group] if entry.get(key) != match_value]

    if len(updated_entries) < len(data[key_group]):
        data[key_group] = updated_entries
        save_json(file_name, data)
        print(f"🗑️ Removed entry with {key} '{match_value}' from {file_name}.")
    else:
        print(f"❌ {key} '{match_value}' not found in {file_name}.")
