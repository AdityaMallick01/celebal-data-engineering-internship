from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List

from scripts.common import parse_order_datetime


def load_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def find_invalid_order_references(order_items_path: Path, orders_path: Path) -> List[Dict[str, str]]:
    orders = load_csv(orders_path)
    valid_order_ids = {row["order_id"] for row in orders}
    invalid_rows: List[Dict[str, str]] = []
    for row in load_csv(order_items_path):
        if row["order_id"] not in valid_order_ids:
            invalid_rows.append(row)
    return invalid_rows


def find_discount_issues(order_items_path: Path) -> List[Dict[str, str]]:
    invalid_rows: List[Dict[str, str]] = []
    for row in load_csv(order_items_path):
        try:
            discount = float(row["discount_percent"])
        except (TypeError, ValueError):
            invalid_rows.append(row)
            continue
        if discount < 0 or discount > 100:
            invalid_rows.append(row)
    return invalid_rows


def find_zero_quantity_rows(order_items_path: Path) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for row in load_csv(order_items_path):
        try:
            quantity = int(float(row["quantity"]))
        except (TypeError, ValueError):
            continue
        if quantity == 0:
            rows.append(row)
    return rows


def find_future_orders(orders_path: Path, reference_datetime: datetime | None = None) -> List[Dict[str, str]]:
    reference_datetime = reference_datetime or datetime.now()
    rows: List[Dict[str, str]] = []
    for row in load_csv(orders_path):
        try:
            order_dt = parse_order_datetime(row["order_date"])
        except ValueError:
            continue
        if order_dt > reference_datetime:
            rows.append(row)
    return rows


def invalid_email_customer_ids(customers_path: Path) -> List[str]:
    invalid_ids: List[str] = []
    rows = load_csv(customers_path)
    for row in rows:
        email = row.get("email", "").strip()
        if not is_valid_email(email):
            invalid_ids.append(row["customer_id"])
    return invalid_ids


def is_valid_email(email: str) -> bool:
    if not email or "@" not in email:
        return False
    local, domain = email.split("@", 1)
    if not local or not domain:
        return False
    if "." not in domain or domain.startswith(".") or domain.endswith("."):
        return False
    return True

