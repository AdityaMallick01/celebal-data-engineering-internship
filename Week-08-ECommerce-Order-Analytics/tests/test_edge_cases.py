from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path
import sys
import unittest

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.common import write_csv  # noqa: E402
from scripts.validation_utils import (  # noqa: E402
    find_discount_issues,
    find_future_orders,
    find_invalid_order_references,
    find_zero_quantity_rows,
)


class EdgeCaseTests(unittest.TestCase):
    def test_invalid_order_reference_detected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            orders_path = temp_path / "orders.csv"
            order_items_path = temp_path / "order_items.csv"
            write_csv(
                orders_path,
                [{"order_id": "O000001", "customer_id": "C0001", "order_date": "2026-01-01 10:00:00", "status": "PLACED", "region_code": "NORTH"}],
                ["order_id", "customer_id", "order_date", "status", "region_code"],
            )
            write_csv(
                order_items_path,
                [{"item_id": "I0000001", "order_id": "O999999", "product_id": "P0001", "quantity": "1", "unit_price": "10.00", "discount_percent": "0"}],
                ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"],
            )
            invalid_rows = find_invalid_order_references(order_items_path, orders_path)
            self.assertEqual(len(invalid_rows), 1)
            self.assertEqual(invalid_rows[0]["order_id"], "O999999")

    def test_discount_percent_over_100_is_flagged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            order_items_path = Path(temp_dir) / "order_items.csv"
            write_csv(
                order_items_path,
                [{"item_id": "I0000002", "order_id": "O000001", "product_id": "P0001", "quantity": "2", "unit_price": "10.00", "discount_percent": "125"}],
                ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"],
            )
            invalid_rows = find_discount_issues(order_items_path)
            self.assertEqual(len(invalid_rows), 1)
            self.assertEqual(invalid_rows[0]["discount_percent"], "125")

    def test_zero_quantity_is_handled_safely(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            order_items_path = Path(temp_dir) / "order_items.csv"
            write_csv(
                order_items_path,
                [{"item_id": "I0000003", "order_id": "O000001", "product_id": "P0001", "quantity": "0", "unit_price": "10.00", "discount_percent": "5"}],
                ["item_id", "order_id", "product_id", "quantity", "unit_price", "discount_percent"],
            )
            zero_rows = find_zero_quantity_rows(order_items_path)
            self.assertEqual(len(zero_rows), 1)
            self.assertEqual(zero_rows[0]["quantity"], "0")

    def test_future_order_date_is_flagged(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            orders_path = Path(temp_dir) / "orders.csv"
            write_csv(
                orders_path,
                [{"order_id": "O000002", "customer_id": "C0001", "order_date": "2099-12-31 23:59:59", "status": "PLACED", "region_code": "SOUTH"}],
                ["order_id", "customer_id", "order_date", "status", "region_code"],
            )
            future_rows = find_future_orders(orders_path, reference_datetime=datetime(2026, 1, 1))
            self.assertEqual(len(future_rows), 1)
            self.assertEqual(future_rows[0]["order_id"], "O000002")


if __name__ == "__main__":
    unittest.main()

