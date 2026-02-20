from properties import create_property
from storage import save_properties, load_properties, save_guests, load_guests, save_bookings, load_bookings
from guests import create_guest
from bookings import create_booking

def main():
    properties = load_properties()
    guests = load_guests()
    while True:
        print("\n1. Add Property")
        print("\n2. View Property")
        print("\n3. Add Guest")
        print("\n4. View Guests")
        print("\n5. Exit")
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

if __name__ == "__main__":
    main()
