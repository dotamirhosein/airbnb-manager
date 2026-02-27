import sqlite3

def get_connection():
    return sqlite3.connect("airbnb.db")

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                rooms INTEGER,
                price_per_night REAL,
                amenities TEXT,
                status TEXT
        )
""")
    
    conn.commit()
    conn.close()

def save_property(prop):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO properties (name, address, rooms, price_per_night, amenities, status)
                VALUES (?, ?, ?, ?, ?, ?)
    """, (
        prop["name"],
        prop["address"],
        prop["rooms"],
        prop["price_per_night"],
        ",".join(prop["amenities"]),
        prop["status"]
    ))

    conn.commit()
    conn.close()

def load_properties():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM properties")
    rows = cursor.fetchall()
    conn.close()
    return [
        {
            "id": r[0],
            "name": r[1],
            "address": r[2],
            "rooms": r[3],
            "price_per_night": r[4],
            "amenities": r[5].split(","),
            "status": r[6]
        }
        for r in rows
    ]

def update_property_status(prop_id, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE properties SET status = ? WHERE id = ?", (status, prop_id))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0  # True اگر آپدیت شد


init_db()
