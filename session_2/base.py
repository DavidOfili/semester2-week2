import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB_PATH = "delivery_demo_light.db"   # or "orders.db" depending on the lab

def get_connection(db_path=DB_PATH):
    return sqlite3.connect(db_path)

def qdf(conn, sql, params=None):
    return pd.read_sql_query(sql, conn, params=params or {})

# -------------------------
# Level 1 – Warm-up
# -------------------------

def t1_list_categories(conn):
    return qdf(conn, """
        SELECT DISTINCT category
        FROM products
        ORDER BY category;
    """)

def t2_count_customers(conn):
    return qdf(conn, "SELECT COUNT(*) AS total_customers FROM customers;")

def t3_orders_for_customer_email(conn, email):
    return qdf(conn, """
        SELECT o.order_id, o.order_date, o.status, o.total_amount
        FROM orders o
        JOIN customers c ON c.customer_id = o.customer_id
        WHERE c.email = :email
        ORDER BY o.order_date DESC;
    """, {"email": email})

def t4_products_below_2(conn):
    return qdf(conn, """
        SELECT product_id, name, category, price
        FROM products
        WHERE price < 2.0
        ORDER BY price ASC;
    """)

# -------------------------
# Level 2 – Basic Analytics
# -------------------------

def t5_top5_total_spent(conn):
    return qdf(conn, """
        SELECT c.customer_id,
               c.first_name || ' ' || c.last_name AS customer_name,
               SUM(o.total_amount) AS total_spent
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY total_spent DESC
        LIMIT 5;
    """)

def t6_orders_per_category(conn, plot=False):
    df = qdf(conn, """
        SELECT p.category,
               COUNT(DISTINCT oi.order_id) AS orders_in_category
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY orders_in_category DESC;
    """)
    if plot:
        df.plot.bar(x="category", y="orders_in_category")
        plt.tight_layout()
        plt.show()
    return df

def t7_avg_products_per_order(conn):
    return qdf(conn, """
        SELECT AVG(items_per_order) AS avg_products_per_order
        FROM (
            SELECT order_id, SUM(quantity) AS items_per_order
            FROM order_items
            GROUP BY order_id
        );
    """)

def t8_deliveries_by_status(conn, plot=False):
    df = qdf(conn, """
        SELECT delivery_status, COUNT(*) AS n
        FROM deliveries
        GROUP BY delivery_status
        ORDER BY n DESC;
    """)
    if plot:
        df.set_index("delivery_status")["n"].plot.pie(autopct="%1.0f%%")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()
    return df

# -------------------------
# Level 3 – Intermediate / Advanced
# -------------------------

def t9_top10_products_by_qty(conn):
    return qdf(conn, """
        SELECT p.product_id, p.name, p.category,
               SUM(oi.quantity) AS total_qty
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.product_id
        ORDER BY total_qty DESC
        LIMIT 10;
    """)

def t10_revenue_per_category(conn, plot=False):
    df = qdf(conn, """
        SELECT p.category,
               SUM(oi.quantity * oi.unit_price) AS total_revenue
        FROM order_items oi
        JOIN products p ON p.product_id = oi.product_id
        GROUP BY p.category
        ORDER BY total_revenue DESC;
    """)
    if plot:
        df.plot.bar(x="category", y="total_revenue")
        plt.tight_layout()
        plt.show()
    return df

def t11_orders_per_delivery_window(conn, plot=False):
    df = qdf(conn, """
        SELECT delivery_window, COUNT(*) AS n_orders
        FROM deliveries
        GROUP BY delivery_window
        ORDER BY n_orders DESC;
    """)
    if plot:
        df.plot.bar(x="delivery_window", y="n_orders")
        plt.tight_layout()
        plt.show()
    return df

def t12_top_customers_by_avg_order_value(conn, limit=5):
    return qdf(conn, """
        SELECT c.customer_id,
               c.first_name || ' ' || c.last_name AS customer_name,
               AVG(o.total_amount) AS avg_order_value,
               COUNT(*) AS num_orders
        FROM customers c
        JOIN orders o ON o.customer_id = c.customer_id
        GROUP BY c.customer_id
        ORDER BY avg_order_value DESC
        LIMIT :limit;
    """, {"limit": limit})

def t13_delivery_performance_by_window(conn):
    return qdf(conn, """
        SELECT delivery_window,
               SUM(CASE WHEN delivery_status = 'delivered' THEN 1 ELSE 0 END) AS delivered,
               SUM(CASE WHEN delivery_status = 'failed' THEN 1 ELSE 0 END) AS failed
        FROM deliveries
        GROUP BY delivery_window
        ORDER BY (delivered + failed) DESC;
    """)

# -------------------------
# Main runner (demo)
# -------------------------

def main():
    conn = get_connection()

    print("\nT1 Categories\n", t1_list_categories(conn))
    print("\nT2 Customer count\n", t2_count_customers(conn))

    # For T3 you need an email that exists in the DB:
    # print("\nT3 Orders for email\n", t3_orders_for_customer_email(conn, "someone@example.com"))

    print("\nT4 Products < £2\n", t4_products_below_2(conn).head())

    print("\nT5 Top 5 spenders\n", t5_top5_total_spent(conn))

    # Plots:
    t6_orders_per_category(conn, plot=True)
    t8_deliveries_by_status(conn, plot=True)
    t10_revenue_per_category(conn, plot=True)

    print("\nT7 Avg products per order\n", t7_avg_products_per_order(conn))
    print("\nT9 Top 10 products by qty\n", t9_top10_products_by_qty(conn))
    print("\nT11 Orders per delivery window\n", t11_orders_per_delivery_window(conn))
    print("\nT12 Top customers by avg order value\n", t12_top_customers_by_avg_order_value(conn))
    print("\nT13 Delivery performance by window\n", t13_delivery_performance_by_window(conn))

    conn.close()

if __name__ == "__main__":
    main()

