import sqlite3
import os

DATABASE = "inventory.db"

def seed_database():
    # If DB exists, remove it to start fresh for demo purposes
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Create the table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL DEFAULT 0
        )
    """)

    # Sample Data
    products = [
        ("P1001", "Wireless Mouse", "Electronics", 50, 499.00),
        ("P1002", "Mechanical Keyboard", "Electronics", 8, 2500.00),
        ("P1003", "USB-C Hub", "Electronics", 0, 1200.00),
        ("P1004", "Notebook A5", "Stationery", 150, 120.00),
        ("P1005", "Ballpoint Pen (Pack)", "Stationery", 300, 45.00),
        ("P1006", "Desk Lamp", "Furniture", 12, 850.00),
        ("P1007", "Monitor Stand", "Furniture", 5, 1500.00),
        ("P1008", "Webcam HD", "Electronics", 25, 3200.00),
        ("P1009", "Stapler", "Stationery", 40, 250.00),
        ("P1010", "Office Chair", "Furniture", 3, 8500.00),
        ("P1011", "Laptop Stand", "Accessories", 18, 1800.00),
        ("P1012", "Power Bank", "Electronics", 60, 1500.00),
        ("P1013", "Whiteboard Marker", "Stationery", 200, 30.00),
        ("P1014", "Cable Organizer", "Accessories", 75, 350.00),
        ("P1015", "External SSD 1TB", "Electronics", 7, 4500.00),
    ]

    # Insert data
    cursor.executemany("""
        INSERT INTO products (product_id, name, category, quantity, price)
        VALUES (?, ?, ?, ?, ?)
    """, products)

    conn.commit()
    conn.close()
    print(f"Database '{DATABASE}' created and seeded with {len(products)} products.")

if __name__ == "__main__":
    seed_database()