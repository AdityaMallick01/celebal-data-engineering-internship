from __future__ import annotations

import argparse
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import (  # noqa: E402
    CLEANED_CUSTOMERS,
    CLEANED_DIR,
    CLEANED_ORDER_ITEMS,
    CLEANED_ORDERS,
    CLEANED_PRODUCTS,
    QUALITY_REPORT_PATH,
    RAW_CUSTOMERS,
    RAW_ORDER_ITEMS,
    RAW_ORDERS,
    RAW_PRODUCTS,
    ensure_directories,
    format_datetime,
    normalize_product_name,
    parse_order_datetime,
    read_csv,
    write_csv,
)
from scripts.validation_utils import (  # noqa: E402
    find_discount_issues,
    find_future_orders,
    find_invalid_order_references,
    find_zero_quantity_rows,
    invalid_email_customer_ids,
    is_valid_email,
)


def clean_orders(input_path: Path = RAW_ORDERS, output_path: Path = CLEANED_ORDERS):
    rows = read_csv(input_path)
    cleaned_rows = []
    corrected_rows = []
    missing_customer_ids = []
    for row in rows:
        raw_date = row["order_date"]
        parsed_date = parse_order_datetime(raw_date)
        normalized_date = format_datetime(parsed_date)
        if raw_date.strip() != normalized_date:
            corrected_rows.append({"order_id": row["order_id"], "from": raw_date, "to": normalized_date})
        row["order_date"] = normalized_date
        if row["customer_id"].strip().upper() == "NULL":
            row["customer_id"] = ""
        if row["customer_id"].strip() == "":
            missing_customer_ids.append(row["order_id"])
        cleaned_rows.append(row)
    write_csv(output_path, cleaned_rows, ["order_id", "customer_id", "order_date", "status", "region_code"])
    return {
        "total_rows": len(rows),
        "missing_customer_count": len(missing_customer_ids),
        "missing_customer_order_ids": missing_customer_ids,
        "corrected_date_count": len(corrected_rows),
        "corrected_dates": corrected_rows,
    }


def clean_products(input_path: Path = RAW_PRODUCTS, output_path: Path = CLEANED_PRODUCTS):
    rows = read_csv(input_path)
    cleaned_rows = []
    normalized_rows = []
    for row in rows:
        raw_name = row["product_name"]
        normalized_name = normalize_product_name(raw_name)
        if raw_name != normalized_name:
            normalized_rows.append({"product_id": row["product_id"], "from": raw_name, "to": normalized_name})
        row["product_name"] = normalized_name
        cleaned_rows.append(row)
    write_csv(output_path, cleaned_rows, ["product_id", "product_name", "category", "subcategory", "cost_price"])
    return {
        "total_rows": len(rows),
        "normalized_count": len(normalized_rows),
        "normalized_products": normalized_rows,
    }


def validate_emails(input_path: Path = RAW_CUSTOMERS):
    rows = read_csv(input_path)
    invalid_ids = []
    for row in rows:
        if not is_valid_email(row.get("email", "").strip()):
            invalid_ids.append(row["customer_id"])
    return invalid_ids


def check_referential_integrity(order_items_path: Path = RAW_ORDER_ITEMS, orders_path: Path = RAW_ORDERS):
    invalid_rows = find_invalid_order_references(order_items_path, orders_path)
    return invalid_rows


def copy_customers(input_path: Path = RAW_CUSTOMERS, output_path: Path = CLEANED_CUSTOMERS):
    rows = read_csv(input_path)
    write_csv(output_path, rows, ["customer_id", "customer_name", "email", "registration_date", "customer_type"])
    return rows


def copy_order_items(input_path: Path = RAW_ORDER_ITEMS, output_path: Path = CLEANED_ORDER_ITEMS):
    rows = read_csv(input_path)
    write_csv(output_path, rows, ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"])
    return rows


def build_quality_report(order_summary, product_summary, invalid_emails, invalid_refs, customers_total, order_items_total, customer_rows, order_item_rows):
    zero_quantity_rows_count = len(find_zero_quantity_rows(RAW_ORDER_ITEMS))
    discount_issues = find_discount_issues(RAW_ORDER_ITEMS)
    future_orders = find_future_orders(RAW_ORDERS)

    lines = []
    lines.append("Week 8 Data Quality Report")
    lines.append("=" * 30)
    lines.append("")
    lines.append("Orders:")
    lines.append(f"  Total rows: {order_summary['total_rows']}")
    lines.append(f"  Missing customer IDs: {order_summary['missing_customer_count']}")
    lines.append(f"  Wrong-format dates corrected: {order_summary['corrected_date_count']}")
    lines.append(f"  Example corrected rows: {order_summary['corrected_dates'][:5]}")
    lines.append("")
    lines.append("Order Items:")
    lines.append(f"  Total rows: {len(order_item_rows)}")
    lines.append(f"  Negative quantity rows (raw): {len([row for row in order_item_rows if int(float(row['quantity'])) < 0])}")
    lines.append(f"  Zero quantity rows: {len([row for row in order_item_rows if int(float(row['quantity'])) == 0])}")
    lines.append(f"  Referential integrity issues: {len(invalid_refs)}")
    lines.append(f"  Discount issues: {len(discount_issues)}")
    lines.append("")
    lines.append("Products:")
    lines.append(f"  Total rows: {product_summary['total_rows']}")
    lines.append(f"  Product names normalized: {product_summary['normalized_count']}")
    lines.append(f"  Example normalized rows: {product_summary['normalized_products'][:5]}")
    lines.append("")
    lines.append("Customers:")
    lines.append(f"  Total rows: {customers_total}")
    lines.append(f"  Invalid emails: {len(invalid_emails)}")
    lines.append(f"  Invalid customer IDs: {invalid_emails[:10]}")
    lines.append("")
    lines.append("Extra validation checks:")
    lines.append(f"  Future orders detected in raw data: {len(future_orders)}")
    lines.append(f"  Zero quantity rows detected in raw data: {zero_quantity_rows_count}")
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description="Clean Week 8 raw data and generate quality report")
    parser.add_argument("--write-report", action="store_true", default=True)
    args = parser.parse_args()

    ensure_directories()
    order_summary = clean_orders()
    product_summary = clean_products()
    customer_rows = copy_customers()
    order_item_rows = copy_order_items()
    invalid_emails = validate_emails()
    invalid_refs = check_referential_integrity()

    report = build_quality_report(
        order_summary=order_summary,
        product_summary=product_summary,
        invalid_emails=invalid_emails,
        invalid_refs=invalid_refs,
        customers_total=len(customer_rows),
        order_items_total=len(order_item_rows),
        customer_rows=customer_rows,
        order_item_rows=order_item_rows,
    )
    QUALITY_REPORT_PATH.write_text(report, encoding="utf-8")

    print("Cleaning complete.")
    print(f"  cleaned orders: {order_summary['total_rows']}")
    print(f"  corrected dates: {order_summary['corrected_date_count']}")
    print(f"  missing customer_ids: {order_summary['missing_customer_count']}")
    print(f"  normalized products: {product_summary['normalized_count']}")
    print(f"  invalid emails: {len(invalid_emails)}")
    print(f"  referential integrity issues: {len(invalid_refs)}")
    print(f"  quality report: {QUALITY_REPORT_PATH}")


if __name__ == "__main__":
    main()
