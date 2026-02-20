from properties import create_property
from storage import save_properties, load_properties, save_guests, load_guests, save_bookings, load_bookings
from guests import create_guest
from bookings import create_booking
from datetime import datetime


def main():
    properties = load_properties()
    guests = load_guests()
    bookings = load_bookings()
    while True:
        print("\n1. Add Property")
        print("\n2. View Property")
        print("\n3. Add Guest")
        print("\n4. View Guests")
        print("\n5. Add Bookings")
        print("\n6. View Bookings")
        print("\n7. Exit")
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
            b = add_booking(properties, guests)
            if b is not None:
                bookings.append(b)
                save_bookings(bookings)
                print("Booking Saved!")
            
        elif choice == "6":
            view_bookings(bookings)
        elif choice == "7":
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

def view_properties(properties):
    if not properties:
        print("No Properties Found.")
        return
    for i, p in enumerate(properties, 1):
        print(f"\n#{i} {p['name']} - {p['address']}")
        print(f"Rooms: {p['rooms']} | Price: ${p['price_per_night']}/night")
        print(f"Amentities: {', '.join(p['amenities'])}")
        print(f"Status: {p['status']}")

def view_guests(guests):
    if not guests:
        print("No guest found.")
        return
    for i, g in enumerate(guests, 1):
        print(f"\n#{i} {g['name']}")
        print(f"Phone: {g['phone']}")
        print(f"Email: {g['email']}")

def add_booking(properties, guests):
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
    
    try:
        start_date_obj = datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
        
        nights = (end_date_obj - start_date_obj).days  # ← اول محاسبه، بعد چک
        
        if nights <= 0:
            print("End date must be after start date!")
            return None
        
        price_per_night = properties[prop_index]["price_per_night"]
        total_price = nights * price_per_night  # ← املای درست
        
        print(f"Total price will be {nights} nights * {price_per_night} = {total_price}")
        
        property_id = prop_index + 1
        guest_id = guest_index + 1
        
        return create_booking(property_id, guest_id, start_date, end_date, total_price)
    
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return None


def view_bookings(bookings):
    if not bookings:
        print("No bookings found.")
        return
    for i, b in enumerate(bookings, 1):
        print(f"\n#{i} Property #{b['property_id']} | Guest #{b['guest_id']}")
        print(f"   From: {b['start_date']} To: {b['end_date']}")
        print(f"   Total price: {b['total_price']}")

if __name__ == "__main__":
    main()
