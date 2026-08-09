from __future__ import annotations

import argparse
import random
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import (  # noqa: E402
    ANALYTICS_SQL_PATH,
    BASE_PRODUCTS,
    CATEGORY_SUBCATEGORY_BUNDLE,
    CLEANED_DIR,
    CLEANED_ORDER_ITEMS,
    CLEANED_ORDERS,
    CLEANED_PRODUCTS,
    CLEANED_CUSTOMERS,
    CUSTOMER_TYPES,
    DATA_DIR,
    DATABASE_PATH,
    EMAIL_DOMAINS,
    FIRST_NAMES,
    LAST_NAMES,
    QUALITY_REPORT_PATH,
    RAW_CUSTOMERS,
    RAW_DATE_END,
    RAW_DIR,
    RAW_ORDER_ITEMS,
    RAW_ORDERS,
    RAW_PRODUCTS,
    REGIONS,
    STATUS_VALUES,
    build_email,
    build_category_product_lookup,
    ensure_directories,
    format_datetime,
    make_dirty_product_name,
    month_key,
    random_datetime,
    revenue_for_row,
    seed_random,
    weighted_choice,
    write_csv,
)

PRODUCT_VARIANTS = ["", "Pro", "Plus", "Max", "Mini", "Prime", "Edge", "Flex", "Lite", "Ultra"]


def build_customers(rng: random.Random, count: int = 600):
    start = datetime(2023, 1, 1, 0, 0, 0)
    end = datetime(2025, 12, 31, 23, 59, 59)
    customers = []
    for index in range(1, count + 1):
        first_name = rng.choice(FIRST_NAMES)
        last_name = rng.choice(LAST_NAMES)
        customer_id = f"C{index:04d}"
        reg_date = random_datetime(rng, start, end)
        customer_type = weighted_choice(rng, CUSTOMER_TYPES, [70, 20, 10])
        region_code = rng.choice(REGIONS)
        customers.append(
            {
                "customer_id": customer_id,
                "customer_name": f"{first_name} {last_name}",
                "email": build_email(first_name, last_name, customer_id, rng),
                "registration_date": format_datetime(reg_date),
                "customer_type": customer_type,
                "_first_name": first_name,
                "_last_name": last_name,
                "_region_code": region_code,
                "_registration_dt": reg_date,
            }
        )
    invalid_indices = set(rng.sample(range(count), max(1, round(count * 0.02))))
    for idx in invalid_indices:
        customer = customers[idx]
        pattern = idx % 3
        if pattern == 0:
            customer["email"] = customer["email"].replace("@", "", 1)
        elif pattern == 1:
            customer["email"] = customer["email"].split("@", 1)[0] + "@"
        else:
            customer["email"] = customer["email"].split("@", 1)[0] + "." + customer["customer_id"].lower()
    return customers


def build_products(rng: random.Random):
    products = []
    product_lookup = defaultdict(list)
    product_id = 1
    for category, base_products in BASE_PRODUCTS.items():
        for base_name, subcategory in base_products:
            for variant in PRODUCT_VARIANTS:
                canonical_name = base_name if not variant else f"{base_name} {variant}"
                cost_low, cost_high = {
                    "Electronics": (35, 260),
                    "Clothing": (12, 95),
                    "Home": (18, 220),
                    "Books": (8, 65),
                }[category]
                base_cost = round(rng.uniform(cost_low, cost_high), 2)
                if variant in {"Pro", "Plus", "Prime", "Ultra"}:
                    base_cost += round(rng.uniform(4, 25), 2)
                product_row = {
                    "product_id": f"P{product_id:04d}",
                    "product_name": canonical_name,
                    "category": category,
                    "subcategory": subcategory,
                    "cost_price": f"{base_cost:.2f}",
                    "_base_name": base_name,
                }
                if rng.random() < 0.18:
                    product_row["product_name"] = make_dirty_product_name(product_row["product_name"], rng)
                products.append(product_row)
                product_lookup[category].append(product_row)
                product_id += 1
    return products, product_lookup


def choose_order_count(rng: random.Random) -> int:
    profile = weighted_choice(rng, ["low", "mid", "high"], [55, 35, 10])
    if profile == "high":
        return rng.randint(8, 11)
    if profile == "mid":
        return rng.randint(4, 6)
    return rng.randint(1, 3)


def select_bundles(rng: random.Random, category: str):
    bundle_pairs = CATEGORY_SUBCATEGORY_BUNDLE[category]
    base_a, base_b = rng.choice(bundle_pairs)
    return base_a, base_b


def pick_product_for_category(rng: random.Random, category: str, product_lookup, popular_only: bool = False):
    rows = product_lookup[category]
    if popular_only:
        rows = rows[: min(20, len(rows))]
    return rng.choice(rows)


def build_orders_and_items(rng: random.Random, customers, product_lookup):
    shift_customers = set(rng.sample([row["customer_id"] for row in customers if row["customer_type"] != "REGULAR"], 120))
    no_delivery_customers = set(rng.sample([row["customer_id"] for row in customers], 12))
    return_prone_customers = set(rng.sample([row["customer_id"] for row in customers], 24))
    return_heavy_products = set()
    for category in product_lookup:
        if len(product_lookup[category]) > 25:
            return_heavy_products.add(product_lookup[category][24]["product_id"])
            return_heavy_products.add(product_lookup[category][25]["product_id"])
    popular_products_by_category = {
        category: [row["product_id"] for row in rows[:20]]
        for category, rows in product_lookup.items()
    }

    orders = []
    order_items = []
    order_id = 1
    item_id = 1
    order_missing_customer_count = 0
    wrong_date_count = 0
    negative_qty_count = 0

    for customer_index, customer in enumerate(customers):
        customer_id = customer["customer_id"]
        order_count = choose_order_count(rng)
        if customer_id in shift_customers and order_count < 2:
            order_count = 2
        registration_dt = customer["_registration_dt"]
        max_days = max(120, (RAW_DATE_END - registration_dt).days)
        offsets = sorted(rng.sample(range(max_days), order_count))
        if rng.random() < 0.65:
            offsets[0] = 0
            offsets = sorted(set(offsets))
            while len(offsets) < order_count:
                offsets.append(rng.randint(1, max_days - 1))
                offsets = sorted(set(offsets))
        if customer_id in shift_customers:
            early_categories = rng.sample(list(product_lookup.keys()), 2)
            late_categories = [cat for cat in product_lookup.keys() if cat not in early_categories]
            if len(late_categories) < 2:
                late_categories = list(product_lookup.keys())
        else:
            early_categories = list(product_lookup.keys())
            late_categories = list(product_lookup.keys())

        for order_idx, day_offset in enumerate(offsets):
            order_dt = registration_dt + timedelta(days=day_offset, hours=rng.randint(0, 23), minutes=rng.randint(0, 59), seconds=rng.randint(0, 59))
            if order_dt > RAW_DATE_END:
                order_dt = RAW_DATE_END - timedelta(days=rng.randint(0, 14), hours=rng.randint(0, 23))
            region_code = customer["_region_code"] if rng.random() < 0.8 else rng.choice(REGIONS)

            if customer_id in shift_customers:
                if order_idx < max(1, order_count // 2):
                    primary_category = rng.choice(early_categories)
                else:
                    primary_category = rng.choice(late_categories)
            else:
                primary_category = weighted_choice(rng, list(product_lookup.keys()), [40, 25, 20, 15])

            if customer_id in no_delivery_customers:
                status = weighted_choice(rng, ["PLACED", "SHIPPED", "CANCELLED", "RETURNED"], [40, 30, 20, 10])
            else:
                status = weighted_choice(rng, STATUS_VALUES, [18, 22, 45, 8, 7])

            order_id_text = f"O{order_id:06d}"
            order_date_text = format_datetime(order_dt)
            if rng.random() < 0.05:
                order_date_text = order_dt.strftime("%d-%m-%Y")
                wrong_date_count += 1
            customer_id_text = customer_id
            if rng.random() < 0.05:
                customer_id_text = ""
                order_missing_customer_count += 1

            orders.append(
                {
                    "order_id": order_id_text,
                    "customer_id": customer_id_text,
                    "order_date": order_date_text,
                    "status": status,
                    "region_code": region_code,
                }
            )

            desired_items = rng.choices([2, 3, 4], weights=[35, 45, 20])[0]
            selected_products = []
            if rng.random() < 0.62:
                base_a, base_b = select_bundles(rng, primary_category)
                bundle_candidates = [row for row in product_lookup[primary_category] if row["_base_name"] in {base_a, base_b}]
                if len(bundle_candidates) >= 2:
                    selected_products.extend([bundle_candidates[0], bundle_candidates[1]])
            while len(selected_products) < desired_items:
                selected_products.append(pick_product_for_category(rng, primary_category, product_lookup, popular_only=True))

            for product in selected_products[:desired_items]:
                unit_cost = float(product["cost_price"])
                unit_price = round(unit_cost * rng.uniform(1.18, 2.45), 2)
                discount = round(rng.uniform(0, 35), 2)
                if product["product_id"] in return_heavy_products:
                    negative_chance = 0.05
                else:
                    negative_chance = 0.01
                if customer_id in return_prone_customers:
                    negative_chance += 0.015
                if status == "RETURNED":
                    negative_chance += 0.04
                if rng.random() < negative_chance:
                    quantity = -rng.randint(2, 5)
                    negative_qty_count += 1
                else:
                    quantity = rng.randint(1, 2) if product["product_id"] in return_heavy_products else rng.randint(1, 5)

                order_items.append(
                    {
                        "item_id": f"I{item_id:07d}",
                        "order_id": order_id_text,
                        "product_id": product["product_id"],
                        "quantity": quantity,
                        "unit_price": f"{unit_price:.2f}",
                        "discount_percent": f"{discount:.2f}",
                    }
                )
                item_id += 1

            order_id += 1

    forced_return_orders = rng.sample(orders, min(len(orders), 96))
    forced_plan = []
    for product_index, product_id in enumerate(sorted(return_heavy_products)):
        forced_plan.extend([(product_id, -rng.randint(3, 5), 0.0)] * 10)
        forced_plan.extend([(product_id, rng.randint(1, 2), 0.0)] * 6)
    rng.shuffle(forced_plan)
    for index, (product_id, quantity, discount) in enumerate(forced_plan):
        order_row = forced_return_orders[index % len(forced_return_orders)]
        item = {
            "item_id": f"I{item_id:07d}",
            "order_id": order_row["order_id"],
            "product_id": product_id,
            "quantity": quantity,
            "unit_price": f"{round(rng.uniform(18, 180), 2):.2f}",
            "discount_percent": f"{discount:.2f}",
        }
        order_items.append(item)
        item_id += 1
        if quantity < 0:
            negative_qty_count += 1

    stats = {
        "orders_total": len(orders),
        "order_items_total": len(order_items),
        "missing_customer_ids": order_missing_customer_count,
        "wrong_date_rows": wrong_date_count,
        "negative_quantity_rows": negative_qty_count,
        "no_delivery_customers": len(no_delivery_customers),
        "shift_customers": len(shift_customers),
        "return_prone_customers": len(return_prone_customers),
        "return_heavy_products": len(return_heavy_products),
    }
    return orders, order_items, stats


def write_raw_outputs(customers, products, orders, order_items):
    customer_rows = [
        {key: value for key, value in row.items() if not key.startswith("_")}
        for row in customers
    ]
    product_rows = [
        {key: value for key, value in row.items() if not key.startswith("_")}
        for row in products
    ]
    write_csv(RAW_CUSTOMERS, customer_rows, ["customer_id", "customer_name", "email", "registration_date", "customer_type"])
    write_csv(RAW_PRODUCTS, product_rows, ["product_id", "product_name", "category", "subcategory", "cost_price"])
    write_csv(RAW_ORDERS, orders, ["order_id", "customer_id", "order_date", "status", "region_code"])
    write_csv(RAW_ORDER_ITEMS, order_items, ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"])


def main():
    parser = argparse.ArgumentParser(description="Generate Week 8 e-commerce CSV data")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--customers", type=int, default=600)
    args = parser.parse_args()

    ensure_directories()
    rng = seed_random(args.seed)
    customers = build_customers(rng, args.customers)
    products, product_lookup = build_products(rng)
    orders, order_items, stats = build_orders_and_items(rng, customers, product_lookup)
    write_raw_outputs(customers, products, orders, order_items)

    print("Generated raw data:")
    print(f"  customers: {len(customers)}")
    print(f"  products: {len(products)}")
    print(f"  orders: {len(orders)}")
    print(f"  order_items: {len(order_items)}")
    print("Intentional issues:")
    print(f"  missing customer_id rows: {stats['missing_customer_ids']}")
    print(f"  wrong-date rows: {stats['wrong_date_rows']}")
    print(f"  negative quantity rows: {stats['negative_quantity_rows']}")
    print(f"  invalid emails: {round(len(customers) * 0.02)}")


if __name__ == "__main__":
    main()
