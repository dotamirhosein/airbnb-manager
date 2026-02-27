def total_income(bookings):
    return sum(b["total_price"] for b in bookings)

def bookings_per_property(bookings, properties):
    prop_names = {p['id']: p['name'] for p in properties}
    counts = {name: 0 for name in prop_names.values()}
    
    for b in bookings:
        prop_id = b['property_id']
        if prop_id in prop_names:
            counts[prop_names[prop_id]] += 1
    
    return counts

def monthly_income(bookings):
    monthly = {}
    for b in bookings:
        year_month = b["start_date"][:7]
        monthly[year_month] = monthly.get(year_month, 0) + b["total_price"]
    return monthly