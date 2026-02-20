def create_booking(property_id, guest_id, start_date, end_date, total_price):
    return {
        "property_id": property_id,
        "guest_id": guest_id,
        "start_date": start_date,
        "end_date": end_date,
        "total_price": total_price
    }
