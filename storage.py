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
    except json.JSONDecodeError:
        return []
    
def save_guests(guests, filename="guests.json"):
    with open(filename, "w") as f:
        json.dump(guests, f, indent=4)

def load_guests(filename="guests.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_bookings(bookings, filename="bookings.json"):
    with open(filename, "w") as f:
        json.dump(bookings, f, indent=4)

def load_bookings(filename="bookings.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []