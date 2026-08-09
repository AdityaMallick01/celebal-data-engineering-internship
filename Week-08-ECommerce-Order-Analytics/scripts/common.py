from __future__ import annotations

import csv
import random
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANED_DIR = DATA_DIR / "cleaned"
SQL_DIR = PROJECT_ROOT / "sql"
DB_DIR = PROJECT_ROOT / "database"
REPORTS_DIR = PROJECT_ROOT / "reports"

RAW_ORDERS = RAW_DIR / "orders.csv"
RAW_ORDER_ITEMS = RAW_DIR / "order_items.csv"
RAW_PRODUCTS = RAW_DIR / "products.csv"
RAW_CUSTOMERS = RAW_DIR / "customers.csv"

CLEANED_ORDERS = CLEANED_DIR / "orders_cleaned.csv"
CLEANED_ORDER_ITEMS = CLEANED_DIR / "order_items_cleaned.csv"
CLEANED_PRODUCTS = CLEANED_DIR / "products_cleaned.csv"
CLEANED_CUSTOMERS = CLEANED_DIR / "customers_cleaned.csv"

DATABASE_PATH = DB_DIR / "ecommerce.db"
QUALITY_REPORT_PATH = REPORTS_DIR / "data_quality_report.txt"
ANALYTICS_SQL_PATH = SQL_DIR / "analytics.sql"

DATE_INPUT_FORMATS = (
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m-%Y",
)

BASE_PRODUCTS = {
    "Electronics": [
        ("Wireless Mouse", "Accessories"),
        ("Mechanical Keyboard", "Accessories"),
        ("Bluetooth Speaker", "Audio"),
        ("Noise Cancelling Headphones", "Audio"),
        ("USB-C Hub", "Computing"),
        ("Laptop Stand", "Computing"),
        ("Portable Charger", "Accessories"),
        ("Smart Watch", "Wearables"),
        ("Webcam", "Computing"),
        ("Gaming Monitor", "Display"),
        ("External SSD", "Storage"),
        ("Router", "Networking"),
        ("Tablet Cover", "Accessories"),
        ("Microphone", "Audio"),
        ("Docking Station", "Computing"),
    ],
    "Clothing": [
        ("Cotton T-Shirt", "Men"),
        ("Denim Jeans", "Men"),
        ("Hooded Sweatshirt", "Unisex"),
        ("Running Shoes", "Footwear"),
        ("Formal Shirt", "Men"),
        ("Summer Dress", "Women"),
        ("Sports Socks", "Accessories"),
        ("Leather Belt", "Accessories"),
        ("Rain Jacket", "Outerwear"),
        ("Polo Shirt", "Men"),
        ("Winter Cap", "Accessories"),
        ("Casual Jacket", "Outerwear"),
        ("Sneakers", "Footwear"),
        ("Formal Trousers", "Men"),
        ("Active Shorts", "Sportswear"),
    ],
    "Home": [
        ("Coffee Maker", "Kitchen"),
        ("Ceramic Mug Set", "Kitchen"),
        ("Desk Lamp", "Decor"),
        ("Storage Basket", "Organization"),
        ("Air Fryer", "Kitchen"),
        ("Vacuum Cleaner", "Cleaning"),
        ("Bed Sheet Set", "Bedding"),
        ("Wall Clock", "Decor"),
        ("Cookware Set", "Kitchen"),
        ("Pillow Set", "Bedding"),
        ("Spice Rack", "Kitchen"),
        ("Floor Mat", "Decor"),
        ("Laundry Basket", "Organization"),
        ("Towel Set", "Bedding"),
        ("Storage Shelf", "Furniture"),
    ],
    "Books": [
        ("Mystery Novel", "Fiction"),
        ("Science Textbook", "Education"),
        ("Recipe Book", "Non-Fiction"),
        ("Journal Notebook", "Stationery"),
        ("History Guide", "Education"),
        ("Language Workbook", "Education"),
        ("Children's Story", "Fiction"),
        ("Travel Guide", "Non-Fiction"),
        ("Study Planner", "Stationery"),
        ("Poetry Collection", "Fiction"),
        ("Coding Manual", "Education"),
        ("Novel Anthology", "Fiction"),
        ("Art Workbook", "Education"),
        ("Business Handbook", "Non-Fiction"),
        ("Comic Collection", "Fiction"),
    ],
}

CATEGORY_SUBCATEGORY_BUNDLE = {
    "Electronics": [
        ("Wireless Mouse", "Mechanical Keyboard"),
        ("USB-C Hub", "Laptop Stand"),
        ("Bluetooth Speaker", "Noise Cancelling Headphones"),
        ("Portable Charger", "Smart Watch"),
    ],
    "Clothing": [
        ("Cotton T-Shirt", "Denim Jeans"),
        ("Running Shoes", "Sports Socks"),
        ("Formal Shirt", "Leather Belt"),
        ("Hooded Sweatshirt", "Casual Jacket"),
    ],
    "Home": [
        ("Coffee Maker", "Ceramic Mug Set"),
        ("Desk Lamp", "Floor Mat"),
        ("Cookware Set", "Spice Rack"),
        ("Bed Sheet Set", "Pillow Set"),
    ],
    "Books": [
        ("Mystery Novel", "Journal Notebook"),
        ("Science Textbook", "Study Planner"),
        ("Recipe Book", "Travel Guide"),
        ("Coding Manual", "Language Workbook"),
    ],
}

FIRST_NAMES = [
    "Aarav", "Aisha", "Anaya", "Arjun", "Diya", "Ishaan", "Kavya", "Meera",
    "Neha", "Rahul", "Riya", "Saanvi", "Shiv", "Tanya", "Vihaan", "Zoya",
    "Aditya", "Bhavna", "Chirag", "Deepa", "Esha", "Farhan", "Gauri", "Harsh",
    "Ira", "Jatin", "Karan", "Lavanya", "Maya", "Nikhil", "Om", "Pooja",
]

LAST_NAMES = [
    "Malhotra", "Patel", "Sharma", "Verma", "Gupta", "Reddy", "Nair", "Khan",
    "Singh", "Iyer", "Joshi", "Kapoor", "Mehta", "Bose", "Chatterjee", "Das",
]

REGIONS = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]
STATUS_VALUES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
CUSTOMER_TYPES = ["REGULAR", "PREMIUM", "VIP"]
EMAIL_DOMAINS = ["example.com", "mail.com", "shopmail.com", "inbox.com"]
RAW_DATE_END = datetime(2026, 6, 30, 23, 59, 59)


def ensure_directories() -> None:
    for path in (RAW_DIR, CLEANED_DIR, SQL_DIR, DB_DIR, REPORTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def seed_random(seed: int = 42) -> random.Random:
    return random.Random(seed)


def write_csv(path: Path, rows: Sequence[Dict[str, object]], fieldnames: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def format_datetime(value: datetime) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S")


def random_datetime(rng: random.Random, start: datetime, end: datetime) -> datetime:
    delta = int((end - start).total_seconds())
    if delta <= 0:
        return start
    return start + timedelta(seconds=rng.randint(0, delta))


def normalize_product_name(value: str) -> str:
    value = re.sub(r"\s+", " ", value.strip())
    return value.title()


def parse_order_datetime(value: str) -> datetime:
    if value is None:
        raise ValueError("Empty order date")
    value = value.strip()
    for fmt in DATE_INPUT_FORMATS:
        try:
            parsed = datetime.strptime(value, fmt)
            if fmt == "%Y-%m-%d":
                return parsed.replace(hour=0, minute=0, second=0)
            if fmt == "%d-%m-%Y":
                return parsed.replace(hour=0, minute=0, second=0)
            return parsed
        except ValueError:
            continue
    raise ValueError(f"Unsupported order date format: {value}")


def build_email(first_name: str, last_name: str, customer_id: str, rng: random.Random) -> str:
    domain = rng.choice(EMAIL_DOMAINS)
    return f"{first_name.lower()}.{last_name.lower()}{customer_id[-2:]}@{domain}"


def make_dirty_product_name(name: str, rng: random.Random) -> str:
    variant = rng.random()
    if variant < 0.33:
        return f" {name.lower()} "
    if variant < 0.66:
        return name.upper() if rng.random() < 0.5 else name.swapcase()
    return name


def weighted_choice(rng: random.Random, values: Sequence[str], weights: Sequence[int]) -> str:
    total = sum(weights)
    pick = rng.uniform(0, total)
    cumulative = 0.0
    for value, weight in zip(values, weights):
        cumulative += weight
        if pick <= cumulative:
            return value
    return values[-1]


def month_start(value: datetime) -> datetime:
    return value.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def month_key(value: datetime) -> str:
    return value.strftime("%Y-%m")


def month_diff(later: datetime, earlier: datetime) -> int:
    return (later.year - earlier.year) * 12 + later.month - earlier.month


def revenue_for_row(quantity: int, unit_price: float, discount_percent: float) -> float:
    return round(quantity * unit_price * (1 - discount_percent / 100.0), 2)


def flatten_bundle_pairs() -> Dict[str, List[tuple[str, str]]]:
    return {category: pairs[:] for category, pairs in CATEGORY_SUBCATEGORY_BUNDLE.items()}


def build_category_product_lookup(products: List[Dict[str, str]]) -> Dict[str, List[Dict[str, str]]]:
    lookup: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for row in products:
        lookup[row["category"]].append(row)
    return lookup
