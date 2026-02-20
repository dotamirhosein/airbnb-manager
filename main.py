from properties import create_property
from storage import save_properties, load_properties

def main():
    properties = load_properties()
    while True:
        print("\n1. Add Property")
        print("\n2. View Property")
        print("\n3. Exit")
        choice = input("Choose: ")
        if choice == "1":
            p = add_property()
            properties.append(p)
            save_properties(properties)
            print("Saved!")
        elif choice == "2":
            view_properties(properties)
        elif choice == "3":
            break

def add_property():
    name = input("Property name: ")
    address = input("Address: ")
    rooms = int(input("Number of Rooms: "))
    price = float(input("Price Per Night: "))
    amenities = input("Amentities (comma Separated,): ").split(",")
    status = input("Status: (Available/Unavailable): ")
    return create_property(name, address, rooms, price, amenities, status)

def view_properties(properties):
    if not properties:
        print("No Properties Found.")
        return
    for i, p in enumerate(properties, 1):
        print(f"\n#{i} {p['name']} - {p['address']}")
        print(f"Rooms: {p['rooms']} | Price: ${p['price_per_night']}/night")
        print(f"Amentities: {', '.join(p['amenities'])}")
        print(f"Status: {p['status']}")

if __name__ == "__main__":
    main()
