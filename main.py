from bookings import create_booking
from properties import create_property
from storage import save_properties, load_properties, save_guests, load_guests, save_bookings, load_bookings
from guests import create_guest
from datetime import datetime
from reports import total_income, bookings_per_property, monthly_income
from validators import is_valid_date, has_conflict


def main():
    properties = load_properties()
    guests = load_guests()
    booking_list = load_bookings()
    while True:
        print("\n1. Add Property")
        print("\n2. View Property")
        print("\n3. Add Guest")
        print("\n4. View Guests")
        print("\n5. Add Bookings")
        print("\n6. View Bookings")
        print("\n7. Total Income")
        print("\n8. Exit")
        choice = input("Choose: ")
        if choice == "1":
            p = add_property()
            properties.append(p)
            save_properties(properties)
            print("Saved!")
        elif choice == "2":
            view_properties(properties)
        elif choice == "3":
            g = add_guest()
            guests.append(g)
            save_guests(guests)
            print("Guest Saved!")
        elif choice == "4":
            view_guests(guests)
        elif choice == "5":
            b = add_booking(properties, guests, booking_list)
            if b is not None:
                booking_list.append(b)
                save_bookings(booking_list)
                print("Booking Saved!")
            
        elif choice == "6":
            view_bookings(booking_list)
        elif choice == "7":
            print(f"Total Income: ${total_income(booking_list):.2f}")
            print("\nBookings per property: ")
            counts = bookings_per_property(booking_list, properties)
            for i, count in enumerate(counts.values(), 1):
                print(f"Property #{i}: {count} bookings.")
            
            print("\nMonthly Income:")
            monthly = monthly_income(booking_list)
            for month, income in sorted(monthly.items()):
                print(f"{month}: ${income:.2f}")
        elif choice == "8":
            break

def add_property():
    name = input("Property name: ")
    address = input("Address: ")
    rooms = int(input("Number of Rooms: "))
    price = float(input("Price Per Night: "))
    amenities = input("Amentities (comma Separated,): ").split(",")
    status = input("Status: (Available/Unavailable): ")
    return create_property(name, address, rooms, price, amenities, status)

def add_guest():
    name = input("Add Guest Name: ")
    phone = int(input("Add Guest Phone-Number: "))
    email = input("Add Guest E-Mail: ")
    return create_guest(name, phone, email)

def view_properties(properties=None):
    if properties is None:
        properties = load_properties()
    if not properties:
        print("No Properties Found.")
        return []
    for i, p in enumerate(properties, 1):
        print(f"\n#{i} {p['name']} - {p['address']}")
        print(f"Rooms: {p['rooms']} | Price: ${p['price_per_night']}/night")
        print(f"Amentities: {', '.join(p['amenities'])}")
        print(f"Status: {p['status']}")
    return properties

def view_guests(guests=None):
    if guests is None:
        guests = load_guests()
    if not guests:
        print("No guest found.")
        return []
    for i, g in enumerate(guests, 1):
        print(f"\n#{i} {g['name']}")
        print(f"Phone: {g['phone']}")
        print(f"Email: {g['email']}")
    return guests

def add_booking(properties, guests, booking_list):
    if not properties:
        print("No properties available for booking.")
        return None
    if not guests:
        print("No guests available for booking.")
        return None
    
    print("\n=== Properties ===")
    view_properties(properties)
    prop_index = int(input("\nSelect Property number: ")) -1 
    
    print("\n=== Guests ===")
    view_guests(guests)
    guest_index = int(input("\nSelect guest number: ")) - 1  
    
    start_date = input("Start date (e.g. 2026-02-20): ")
    end_date = input("End date (e.g. 2026-02-22): ")

    if not is_valid_date(start_date) or not is_valid_date(end_date):
        print("Invalid Date Format!")
        return None
    
    if has_conflict(start_date, end_date, booking_list, prop_index + 1):
        print("Property is already booked for some/all of these dates!")
        return None
    
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        nights = (end_date_obj - start_date_obj).days 
        if nights <= 0:
            print("End date must be after start date!")
            return None
        
        price_per_night = properties[prop_index]["price_per_night"]
        total_price = nights * price_per_night 
        
        print(f"Total price will be {nights} nights * {price_per_night} = {total_price}")
        
        property_id = prop_index + 1
        guest_id = guest_index + 1
        
        return create_booking(property_id, guest_id, start_date, end_date, total_price)
    
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None

def view_bookings(bookings=None):
    if bookings is None:
        bookings = load_bookings()
    if not bookings:
        print("No bookings found.")
        return []
    for i, b in enumerate(bookings, 1):
        print(f"\n#{i} Property #{b['property_id']} | Guest #{b['guest_id']}")
        print(f"   From: {b['start_date']} To: {b['end_date']}")
        print(f"   Total price: {b['total_price']}")
    return bookings


if __name__ == "__main__":
    main()
