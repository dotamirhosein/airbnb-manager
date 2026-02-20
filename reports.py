def total_income(bookings):
    return sum(b["total_price"] for b in bookings)

def bookings_per_property(bookings, properties):
    count = {}
    property_booking = {i: 0 for i in range(len(properties))}
    for b in bookings:
        prop_id = b["property_id"] 
        property_booking[prop_id - 1] += 1
    return property_booking

def monthly_income(bookings):
    monthly = {}
    for b in bookings:
        year_month = b["start_date"][:7]
        monthly[year_month] = monthly.get(year_month, 0) + b["total_price"]
    return monthly