from flask import Flask, request, jsonify, render_template  # type: ignore[reportMissingImports]
import sqlite3

app = Flask(__name__)

DATABASE = "inventory.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_db_connection()
    
    # Create table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            price REAL NOT NULL DEFAULT 0
        )
    """)
    
    # Check if table is empty
    count = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    
    if count == 0:
        print("Database is empty. Seeding with sample data...")
        # Re-use the same logic as seed.py or import it
        # For simplicity, just insert here or call a seed function
        products = [
            ("P1001", "Wireless Mouse", "Electronics", 50, 499.00),
            ("P1002", "Mechanical Keyboard", "Electronics", 8, 2500.00),
            ("P1003", "USB-C Hub", "Electronics", 0, 1200.00),
            # ... add the rest of your sample data here ...
        ]
        conn.executemany("""
            INSERT INTO products (product_id, name, category, quantity, price)
            VALUES (?, ?, ?, ?)
        """, products)
        conn.commit()

    conn.close()


@app.route("/")
def home():
    return render_template("index.html")


# Get all products / search products
@app.route("/api/products", methods=["GET"])
def get_products():
    search = request.args.get("search", "").strip()

    conn = get_db_connection()

    if search:
        products = conn.execute("""
            SELECT * FROM products
            WHERE product_id LIKE ?
               OR name LIKE ?
               OR category LIKE ?
            ORDER BY id DESC
        """, (
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        )).fetchall()
    else:
        products = conn.execute("""
            SELECT * FROM products
            ORDER BY id DESC
        """).fetchall()

    conn.close()

    return jsonify([dict(product) for product in products])


# Add product
@app.route("/api/products", methods=["POST"])
def add_product():
    data = request.get_json()

    product_id = str(data.get("product_id", "")).strip()
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "")).strip()

    try:
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0))
    except (ValueError, TypeError):
        return jsonify({
            "error": "Quantity must be an integer and price must be a number."
        }), 400

    if not product_id or not name or not category:
        return jsonify({
            "error": "All required fields must be filled."
        }), 400

    if quantity < 0:
        return jsonify({
            "error": "Quantity cannot be negative."
        }), 400

    if price < 0:
        return jsonify({
            "error": "Price cannot be negative."
        }), 400

    conn = get_db_connection()

    try:
        conn.execute("""
            INSERT INTO products
            (product_id, name, category, quantity, price)
            VALUES (?, ?, ?, ?, ?)
        """, (
            product_id,
            name,
            category,
            quantity,
            price
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        conn.close()

        return jsonify({
            "error": "Product ID already exists."
        }), 409

    conn.close()

    return jsonify({
        "message": "Product added successfully."
    }), 201


# Update product
@app.route("/api/products/<int:id>", methods=["PUT"])
def update_product(id):
    data = request.get_json()

    product_id = str(data.get("product_id", "")).strip()
    name = str(data.get("name", "")).strip()
    category = str(data.get("category", "")).strip()

    try:
        quantity = int(data.get("quantity", 0))
        price = float(data.get("price", 0))
    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid quantity or price."
        }), 400

    if not product_id or not name or not category:
        return jsonify({
            "error": "All required fields must be filled."
        }), 400

    if quantity < 0 or price < 0:
        return jsonify({
            "error": "Quantity and price cannot be negative."
        }), 400

    conn = get_db_connection()

    existing = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (id,)
    ).fetchone()

    if not existing:
        conn.close()

        return jsonify({
            "error": "Product not found."
        }), 404

    duplicate = conn.execute(
        "SELECT id FROM products WHERE product_id = ? AND id != ?",
        (product_id, id)
    ).fetchone()

    if duplicate:
        conn.close()

        return jsonify({
            "error": "Another product already uses this Product ID."
        }), 409

    conn.execute("""
        UPDATE products
        SET product_id = ?,
            name = ?,
            category = ?,
            quantity = ?,
            price = ?
        WHERE id = ?
    """, (
        product_id,
        name,
        category,
        quantity,
        price,
        id
    ))

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Product updated successfully."
    })


# Delete product
@app.route("/api/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = get_db_connection()

    product = conn.execute(
        "SELECT * FROM products WHERE id = ?",
        (id,)
    ).fetchone()

    if not product:
        conn.close()

        return jsonify({
            "error": "Product not found."
        }), 404

    conn.execute(
        "DELETE FROM products WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Product deleted successfully."
    })


# Dashboard statistics
@app.route("/api/stats", methods=["GET"])
def get_stats():
    conn = get_db_connection()

    total_products = conn.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    total_stock = conn.execute(
        "SELECT COALESCE(SUM(quantity), 0) FROM products"
    ).fetchone()[0]

    low_stock = conn.execute(
        "SELECT COUNT(*) FROM products WHERE quantity < 10"
    ).fetchone()[0]

    inventory_value = conn.execute(
        "SELECT COALESCE(SUM(quantity * price), 0) FROM products"
    ).fetchone()[0]

    conn.close()

    return jsonify({
        "total_products": total_products,
        "total_stock": total_stock,
        "low_stock": low_stock,
        "inventory_value": inventory_value
    })


if __name__ == "__main__":
    initialize_database()
    app.run(debug=True)
