USE celebal_week2;

-- ==========================================
-- Indexes for customers
-- ==========================================
CREATE INDEX idx_customers_city
ON customers(city);

CREATE INDEX idx_customers_state
ON customers(state);

-- ==========================================
-- Indexes for products
-- ==========================================
CREATE INDEX idx_products_category
ON products(category);

-- ==========================================
-- Indexes for orders
-- ==========================================
CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_orders_status
ON orders(status);