from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
import sys

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import DATABASE_PATH  # noqa: E402


def parse_date(value: str) -> datetime:
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("Dates must use YYYY-MM-DD format.") from exc


def fetch_scalar(conn: sqlite3.Connection, query: str, params: tuple) -> float:
    value = conn.execute(query, params).fetchone()[0]
    return 0 if value is None else value


def period_bounds(start_date: datetime, end_date: datetime) -> tuple[datetime, datetime, datetime, datetime]:
    if end_date < start_date:
        raise ValueError("End date must be on or after start date.")
    period_days = (end_date - start_date).days + 1
    prev_end = start_date - timedelta(days=1)
    prev_start = prev_end - timedelta(days=period_days - 1)
    return start_date, end_date, prev_start, prev_end


def summarize_period(conn: sqlite3.Connection, start_date: datetime, end_date: datetime):
    start_text = start_date.strftime("%Y-%m-%d")
    end_text = end_date.strftime("%Y-%m-%d")
    total_orders = fetch_scalar(
        conn,
        """
        SELECT COUNT(DISTINCT o.order_id)
        FROM orders o
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
        """,
        (start_text, end_text),
    )
    revenue = fetch_scalar(
        conn,
        """
        SELECT COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0)
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
        """,
        (start_text, end_text),
    )
    unique_customers = fetch_scalar(
        conn,
        """
        SELECT COUNT(DISTINCT o.customer_id)
        FROM orders o
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
          AND o.customer_id IS NOT NULL AND o.customer_id <> ''
        """,
        (start_text, end_text),
    )
    top_products = conn.execute(
        """
        SELECT p.product_name,
               ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS revenue
        FROM orders o
        JOIN order_items oi ON oi.order_id = o.order_id
        JOIN products p ON p.product_id = oi.product_id
        WHERE date(o.order_date) BETWEEN date(?) AND date(?)
        GROUP BY p.product_name
        ORDER BY revenue DESC, p.product_name
        LIMIT 3
        """,
        (start_text, end_text),
    ).fetchall()
    return {
        "total_orders": int(total_orders),
        "revenue": float(revenue),
        "unique_customers": int(unique_customers),
        "top_products": top_products,
    }


def percent_change(current: float, previous: float):
    if previous in (0, 0.0):
        return "N/A"
    return f"{((current - previous) / previous) * 100:.2f}%"


def print_report(report_type: str, start_date: datetime, end_date: datetime, summary, previous_summary):
    print(f"Week 8 {report_type.title()} Report")
    print(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print("-" * 50)
    print(f"Total orders: {summary['total_orders']} ({percent_change(summary['total_orders'], previous_summary['total_orders'])} vs previous period)")
    print(f"Revenue: {summary['revenue']:.2f} ({percent_change(summary['revenue'], previous_summary['revenue'])} vs previous period)")
    print(f"Unique customers: {summary['unique_customers']} ({percent_change(summary['unique_customers'], previous_summary['unique_customers'])} vs previous period)")
    print("Top 3 products:")
    if summary["top_products"]:
        for index, (product_name, revenue) in enumerate(summary["top_products"], 1):
            print(f"  {index}. {product_name} - {float(revenue):.2f}")
    else:
        print("  No products found for the selected period.")


def main():
    parser = argparse.ArgumentParser(description="Week 8 SQLite report generator")
    parser.add_argument("report_type", help="daily, weekly, or monthly")
    parser.add_argument("start_date", help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", help="End date in YYYY-MM-DD format")
    parser.add_argument("--db", type=Path, default=DATABASE_PATH)
    args = parser.parse_args()

    if args.report_type.lower() not in {"daily", "weekly", "monthly"}:
        print("Invalid report type. Use daily, weekly, or monthly.", file=sys.stderr)
        raise SystemExit(1)

    try:
        start_date = parse_date(args.start_date)
        end_date = parse_date(args.end_date)
        start_date, end_date, prev_start, prev_end = period_bounds(start_date, end_date)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)

    if not args.db.exists():
        print(f"Database not found: {args.db}", file=sys.stderr)
        raise SystemExit(1)

    with sqlite3.connect(args.db) as conn:
        summary = summarize_period(conn, start_date, end_date)
        previous_summary = summarize_period(conn, prev_start, prev_end)
        print_report(args.report_type.lower(), start_date, end_date, summary, previous_summary)


if __name__ == "__main__":
    main()

