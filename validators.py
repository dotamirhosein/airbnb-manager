from datetime import datetime


def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def has_conflict(new_start, new_end, existing_bookings, property_id):
    for b in existing_bookings:
        if b["property_id"] != property_id:
            continue
            
        if (new_start < b["end_date"] and 
            new_end > b["start_date"]):
            return True
    return False