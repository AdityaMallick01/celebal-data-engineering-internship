-- 01. Total revenue per category
SELECT
    p.category,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_revenue
FROM order_items oi
JOIN products p ON p.product_id = oi.product_id
GROUP BY p.category
ORDER BY total_revenue DESC, p.category;

-- 02. Top 10 customers by total order value
SELECT
    c.customer_id,
    c.customer_name,
    ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS total_order_value
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_order_value DESC, c.customer_id
LIMIT 10;

-- 03. Month-wise order count for the last 12 months represented by the dataset
WITH RECURSIVE month_bounds AS (
    SELECT date(MAX(date(order_date)), 'start of month') AS last_month
    FROM orders
),
months(month_start) AS (
    SELECT date((SELECT last_month FROM month_bounds), '-11 months')
    UNION ALL
    SELECT date(month_start, '+1 month')
    FROM months
    WHERE month_start < (SELECT last_month FROM month_bounds)
)
SELECT
    strftime('%Y-%m', months.month_start) AS year_month,
    COUNT(o.order_id) AS order_count
FROM months
LEFT JOIN orders o
    ON date(o.order_date, 'start of month') = months.month_start
GROUP BY months.month_start
ORDER BY months.month_start;

-- 04. Customers who ordered but never had any item delivered
SELECT
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS order_count
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
HAVING SUM(CASE WHEN o.status = 'DELIVERED' THEN 1 ELSE 0 END) = 0
ORDER BY order_count DESC, c.customer_id;

-- 05. Products ordered but with more returns than purchases
WITH product_flow AS (
    SELECT
        p.product_id,
        p.product_name,
        SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchase_qty,
        SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS return_qty
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    GROUP BY p.product_id, p.product_name
)
SELECT
    product_id,
    product_name,
    purchase_qty,
    return_qty,
    (return_qty - purchase_qty) AS return_minus_purchase
FROM product_flow
WHERE return_qty > purchase_qty
ORDER BY return_minus_purchase DESC, product_name;

-- 06. Return rate per category
WITH category_items AS (
    SELECT
        p.category,
        SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returned_items,
        SUM(ABS(oi.quantity)) AS total_items
    FROM order_items oi
    JOIN products p ON p.product_id = oi.product_id
    GROUP BY p.category
)
SELECT
    category,
    returned_items,
    total_items,
    ROUND(1.0 * returned_items / NULLIF(total_items, 0), 4) AS return_rate
FROM category_items
ORDER BY return_rate DESC, category;

-- 07. Running total with window function
WITH daily_region_revenue AS (
    SELECT
        o.region_code,
        date(o.order_date) AS order_date,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY o.region_code, date(o.order_date)
)
SELECT
    region_code,
    order_date,
    daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY region_code
        ORDER BY order_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM daily_region_revenue
ORDER BY region_code, order_date;

-- 08. DENSE_RANK product ranking
WITH category_product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        ROUND(
            SUM(
                oi.quantity
                * oi.unit_price
                * (1 - oi.discount_percent / 100.0)
            ),
            2
        ) AS total_revenue
    FROM order_items oi
    JOIN products p
        ON p.product_id = oi.product_id
    GROUP BY
        p.category,
        p.product_name
)
SELECT
    category,
    product_name,
    total_revenue,
    DENSE_RANK() OVER (
        PARTITION BY category
        ORDER BY total_revenue DESC
    ) AS rank_in_category
FROM category_product_revenue
ORDER BY
    category,
    rank_in_category,
    product_name;
    
-- 09. LAG / LEAD analysis
WITH customer_order_dates AS (
    SELECT
        o.customer_id,
        date(o.order_date) AS order_date,
        LAG(date(o.order_date)) OVER (
            PARTITION BY o.customer_id
            ORDER BY date(o.order_date)
        ) AS previous_order_date
    FROM orders o
    WHERE o.customer_id IS NOT NULL AND o.customer_id <> ''
),
customer_gaps AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,
        CASE
            WHEN previous_order_date IS NULL THEN NULL
            ELSE CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
        END AS days_gap
    FROM customer_order_dates
),
customer_avg_gap AS (
    SELECT
        customer_id,
        ROUND(AVG(days_gap), 2) AS avg_gap_days
    FROM customer_gaps
    WHERE days_gap IS NOT NULL
    GROUP BY customer_id
)
SELECT
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    c.avg_gap_days,
    CASE WHEN c.avg_gap_days > 30 THEN 'At Risk' ELSE 'Healthy' END AS risk_status
FROM customer_gaps g
LEFT JOIN customer_avg_gap c ON c.customer_id = g.customer_id
ORDER BY g.customer_id, g.order_date;

-- 10. Multi-level CTE customer categorization
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS revenue_month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.customer_id IS NOT NULL AND o.customer_id <> ''
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
),
categorized_customers AS (
    SELECT
        customer_id,
        revenue_month,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue BETWEEN 5000 AND 10000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_band
    FROM monthly_customer_revenue
)
SELECT
    revenue_month,
    revenue_band,
    COUNT(*) AS customer_count
FROM categorized_customers
GROUP BY revenue_month, revenue_band
ORDER BY revenue_month, revenue_band;

-- 11. NTILE segmentation
WITH lifetime_value AS (
    SELECT
        c.customer_id,
        ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0), 2) AS total_value
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.customer_id
)
SELECT
    customer_id,
    total_value,
    NTILE(4) OVER (ORDER BY total_value DESC, customer_id) AS quartile,
    CASE NTILE(4) OVER (ORDER BY total_value DESC, customer_id)
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        ELSE 'Bronze'
    END AS quartile_label
FROM lifetime_value
ORDER BY quartile, total_value DESC, customer_id;

-- 12. Year-over-year comparison
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY CAST(strftime('%Y', o.order_date) AS INTEGER), CAST(strftime('%m', o.order_date) AS INTEGER)
),
previous_year AS (
    SELECT
        year + 1 AS year,
        month,
        revenue AS prev_year_revenue
    FROM monthly_revenue
)
SELECT
    m.year,
    m.month,
    m.revenue,
    py.prev_year_revenue,
    CASE
        WHEN py.prev_year_revenue IS NULL OR py.prev_year_revenue = 0 THEN NULL
        ELSE ROUND(((m.revenue - py.prev_year_revenue) / py.prev_year_revenue) * 100.0, 2)
    END AS yoy_growth_percent
FROM monthly_revenue m
LEFT JOIN previous_year py
    ON py.year = m.year
   AND py.month = m.month
ORDER BY m.year, m.month;

-- 13. First/last value analysis
WITH customer_category_history AS (
    SELECT
        o.customer_id,
        date(o.order_date) AS order_date,
        p.category,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY date(o.order_date), o.order_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_category,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id
            ORDER BY date(o.order_date) DESC, o.order_id DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_category,
        ROW_NUMBER() OVER (
            PARTITION BY o.customer_id
            ORDER BY date(o.order_date) DESC, o.order_id DESC
        ) AS rn
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    JOIN products p ON p.product_id = oi.product_id
    WHERE o.customer_id IS NOT NULL AND o.customer_id <> ''
)
SELECT DISTINCT
    customer_id,
    first_category,
    last_category,
    CASE WHEN first_category <> last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM customer_category_history
WHERE rn = 1
ORDER BY customer_id;

-- 14. Cumulative distribution
WITH customer_revenue AS (
    SELECT
        c.customer_id,
        ROUND(COALESCE(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 0), 2) AS revenue
    FROM customers c
    LEFT JOIN orders o ON o.customer_id = c.customer_id
    LEFT JOIN order_items oi ON oi.order_id = o.order_id
    GROUP BY c.customer_id
),
ranked AS (
    SELECT
        customer_id,
        revenue,
        SUM(revenue) OVER (
            ORDER BY revenue DESC, customer_id
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) AS cumulative_revenue,
        SUM(revenue) OVER () AS total_revenue
    FROM customer_revenue
)
SELECT
    customer_id,
    revenue,
    cumulative_revenue,
    ROUND(1.0 * cumulative_revenue / NULLIF(total_revenue, 0), 4) AS cumulative_percent
FROM ranked
ORDER BY revenue DESC, customer_id;

-- 15. Cohort analysis
WITH customer_monthly_orders AS (
    SELECT
        c.customer_id,
        date(c.registration_date, 'start of month') AS cohort_month,
        ((CAST(strftime('%Y', o.order_date) AS INTEGER) - CAST(strftime('%Y', c.registration_date) AS INTEGER)) * 12
         + (CAST(strftime('%m', o.order_date) AS INTEGER) - CAST(strftime('%m', c.registration_date) AS INTEGER))) AS month_offset
    FROM customers c
    JOIN orders o ON o.customer_id = c.customer_id
    WHERE o.customer_id IS NOT NULL AND o.customer_id <> ''
),
cohort_counts AS (
    SELECT
        cohort_month,
        month_offset,
        COUNT(DISTINCT customer_id) AS customer_count
    FROM customer_monthly_orders
    WHERE month_offset BETWEEN 0 AND 3
    GROUP BY cohort_month, month_offset
),
cohort_pivot AS (
    SELECT
        cohort_month,
        MAX(CASE WHEN month_offset = 0 THEN customer_count END) AS month_0_customers,
        MAX(CASE WHEN month_offset = 1 THEN customer_count END) AS month_1_customers,
        MAX(CASE WHEN month_offset = 2 THEN customer_count END) AS month_2_customers,
        MAX(CASE WHEN month_offset = 3 THEN customer_count END) AS month_3_customers
    FROM cohort_counts
    GROUP BY cohort_month
)
SELECT
    cohort_month,
    COALESCE(month_0_customers, 0) AS month_0_customers,
    COALESCE(month_1_customers, 0) AS month_1_customers,
    COALESCE(month_2_customers, 0) AS month_2_customers,
    COALESCE(month_3_customers, 0) AS month_3_customers,
    ROUND(1.0 * COALESCE(month_1_customers, 0) / NULLIF(month_0_customers, 0), 4) AS retention_month_1,
    ROUND(1.0 * COALESCE(month_2_customers, 0) / NULLIF(month_0_customers, 0), 4) AS retention_month_2,
    ROUND(1.0 * COALESCE(month_3_customers, 0) / NULLIF(month_0_customers, 0), 4) AS retention_month_3
FROM cohort_pivot
ORDER BY cohort_month;

-- 16. Frequently bought together
SELECT
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    COUNT(DISTINCT a.order_id) AS times_bought_together
FROM order_items a
JOIN order_items b
    ON a.order_id = b.order_id
   AND a.product_id < b.product_id
JOIN products p1 ON p1.product_id = a.product_id
JOIN products p2 ON p2.product_id = b.product_id
GROUP BY p1.product_name, p2.product_name
HAVING times_bought_together > 0
ORDER BY times_bought_together DESC, product_a, product_b;

