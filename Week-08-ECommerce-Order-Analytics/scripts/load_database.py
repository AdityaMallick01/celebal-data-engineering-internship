from __future__ import annotations

import argparse
import csv
import sqlite3
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import (  # noqa: E402
    CLEANED_CUSTOMERS,
    CLEANED_ORDER_ITEMS,
    CLEANED_ORDERS,
    CLEANED_PRODUCTS,
    DATABASE_PATH,
    ensure_directories,
)


def load_csv_rows(path: Path):
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def create_tables(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;

        CREATE TABLE customers (
            customer_id TEXT PRIMARY KEY,
            customer_name TEXT NOT NULL,
            email TEXT NOT NULL,
            registration_date TEXT NOT NULL,
            customer_type TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT NOT NULL,
            cost_price REAL NOT NULL
        );

        CREATE TABLE orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NULL,
            order_date TEXT NOT NULL,
            status TEXT NOT NULL,
            region_code TEXT NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );

        CREATE TABLE order_items (
            item_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            discount_percent REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )
    conn.executescript(
        """
        CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON orders(customer_id);
        CREATE INDEX IF NOT EXISTS idx_orders_order_date ON orders(order_date);
        CREATE INDEX IF NOT EXISTS idx_orders_region_code ON orders(region_code);
        CREATE INDEX IF NOT EXISTS idx_order_items_order_id ON order_items(order_id);
        CREATE INDEX IF NOT EXISTS idx_order_items_product_id ON order_items(product_id);
        CREATE INDEX IF NOT EXISTS idx_products_category ON products(category);
        """
    )


def insert_customers(conn: sqlite3.Connection, path: Path) -> int:
    rows = load_csv_rows(path)
    conn.executemany(
        "INSERT INTO customers (customer_id, customer_name, email, registration_date, customer_type) VALUES (?, ?, ?, ?, ?)",
        [(row["customer_id"], row["customer_name"], row["email"], row["registration_date"], row["customer_type"]) for row in rows],
    )
    return len(rows)


def insert_products(conn: sqlite3.Connection, path: Path) -> int:
    rows = load_csv_rows(path)
    conn.executemany(
        "INSERT INTO products (product_id, product_name, category, subcategory, cost_price) VALUES (?, ?, ?, ?, ?)",
        [(row["product_id"], row["product_name"], row["category"], row["subcategory"], float(row["cost_price"])) for row in rows],
    )
    return len(rows)


def insert_orders(conn: sqlite3.Connection, path: Path) -> int:
    rows = load_csv_rows(path)
    prepared = []
    for row in rows:
        customer_id = row["customer_id"].strip()
        prepared.append(
            (
                row["order_id"],
                customer_id if customer_id else None,
                row["order_date"],
                row["status"],
                row["region_code"],
            )
        )
    conn.executemany(
        "INSERT INTO orders (order_id, customer_id, order_date, status, region_code) VALUES (?, ?, ?, ?, ?)",
        prepared,
    )
    return len(rows)


def insert_order_items(conn: sqlite3.Connection, path: Path) -> int:
    rows = load_csv_rows(path)
    conn.executemany(
        "INSERT INTO order_items (item_id, order_id, product_id, quantity, unit_price, discount_percent) VALUES (?, ?, ?, ?, ?, ?)",
        [
            (
                row["item_id"],
                row["order_id"],
                row["product_id"],
                int(float(row["quantity"])),
                float(row["unit_price"]),
                float(row["discount_percent"]),
            )
            for row in rows
        ],
    )
    return len(rows)


def load_database(db_path: Path = DATABASE_PATH) -> dict[str, int]:
    ensure_directories()
    if db_path.exists():
        db_path.unlink()
    with sqlite3.connect(db_path) as conn:
        create_tables(conn)
        customer_count = insert_customers(conn, CLEANED_CUSTOMERS)
        product_count = insert_products(conn, CLEANED_PRODUCTS)
        order_count = insert_orders(conn, CLEANED_ORDERS)
        order_item_count = insert_order_items(conn, CLEANED_ORDER_ITEMS)
        conn.commit()
    return {
        "customers": customer_count,
        "products": product_count,
        "orders": order_count,
        "order_items": order_item_count,
    }


def main():
    parser = argparse.ArgumentParser(description="Load Week 8 cleaned data into SQLite")
    parser.add_argument("--db", type=Path, default=DATABASE_PATH)
    args = parser.parse_args()

    counts = load_database(args.db)
    print("SQLite load complete.")
    for key, value in counts.items():
        print(f"  {key}: {value}")
    print(f"  database: {args.db}")


if __name__ == "__main__":
    main()

