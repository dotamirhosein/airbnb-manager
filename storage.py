import json

def save_properties(properties, filename="properties.json"):
    with open(filename, "w") as f:
        json.dump(properties, f, indent=4)

def load_properties(filename="properties.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []