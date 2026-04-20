# Inventory API Full Test Script

from pprint import pprint
from datetime import datetime, timedelta

from core.client import APIClient


BASE_URL = "http://localhost:8000"
USERNAME = "admin.app@example.com"
PASSWORD = "secretpassword"


def print_section(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


client = APIClient(base_url=BASE_URL)


# =========================================================
# AUTHENTICATION
# =========================================================
print_section("AUTHENTICATION")

login_result = client.login(
    username=USERNAME,
    password=PASSWORD
)
pprint(login_result)

me_result = client.me()
pprint(me_result)


# =========================================================
# CREATE TEST DATA
# =========================================================
print_section("CREATE TEST DATA")

# Categories
category_1 = client.create_category("Electronics")
category_2 = client.create_category("Office Supplies")
category_3 = client.create_category("Home Appliances")

pprint(category_1)
pprint(category_2)
pprint(category_3)

categories = client.get_all_categories()
pprint(categories)

category_ids = [c["category_id"] for c in categories.get("categories", [])]

category_id_1 = category_ids[0]
category_id_2 = category_ids[1]
category_id_3 = category_ids[2]


# Warehouses
warehouse_1 = client.create_warehouse(
    name="Main Warehouse",
    location="Mexico City"
)
warehouse_2 = client.create_warehouse(
    name="North Warehouse",
    location="Monterrey"
)

pprint(warehouse_1)
pprint(warehouse_2)

warehouses = client.get_all_warehouses()
pprint(warehouses)

warehouse_ids = [w["warehouse_id"] for w in warehouses.get("warehouses", [])]

warehouse_id_1 = warehouse_ids[0]
warehouse_id_2 = warehouse_ids[1]


# Suppliers
supplier_1 = client.create_supplier(
    name="Tech Supplier SA",
    contact_info="tech@example.com"
)
supplier_2 = client.create_supplier(
    name="Office Goods MX",
    contact_info="office@example.com"
)

pprint(supplier_1)
pprint(supplier_2)

suppliers = client.get_all_suppliers()
pprint(suppliers)

supplier_ids = [s["supplier_id"] for s in suppliers.get("suppliers", [])]

supplier_id_1 = supplier_ids[0]


# Products
product_1 = client.create_product(
    name="Laptop Pro 15",
    description="High performance laptop",
    sku="LAP-001",
    category_id=category_id_1,
    unit_price=25000.0
)

product_2 = client.create_product(
    name="Wireless Mouse",
    description="Ergonomic wireless mouse",
    sku="MOU-001",
    category_id=category_id_1,
    unit_price=500.0
)

product_3 = client.create_product(
    name="Printer Paper Pack",
    description="500 sheets paper pack",
    sku="PAP-001",
    category_id=category_id_2,
    unit_price=150.0
)

pprint(product_1)
pprint(product_2)
pprint(product_3)

products = client.get_all_products()
pprint(products)

product_ids = [p["product_id"] for p in products.get("products", [])]

product_id_1 = product_ids[0]
product_id_2 = product_ids[1]
product_id_3 = product_ids[2]


# User
new_user = client.create_user(
    name="Test Manager",
    email="manager@example.com",
    password="manager123",
    permission_level="admin"
)
pprint(new_user)

users = client.get_all_users()
pprint(users)

user_ids = [u["user_id"] for u in users.get("users", [])]
new_user_id = user_ids[-1]


# =========================================================
# UPDATE TESTS
# =========================================================
print_section("UPDATE TESTS")

pprint(client.update_category(
    category_id=category_id_1,
    name="Electronics & Gadgets"
))

pprint(client.update_product(
    product_id=product_id_1,
    name="Laptop Pro 16",
    description="Updated laptop model",
    sku="LAP-002",
    category_id=category_id_1,
    unit_price=27000.0
))

pprint(client.update_warehouse(
    warehouse_id=warehouse_id_1,
    name="Central Warehouse",
    location="Guadalajara"
))

pprint(client.update_supplier(
    supplier_id=supplier_id_1,
    name="Tech Supplier International",
    contact_info="support@techsupplier.com"
))

pprint(client.update_user(
    user_id=new_user_id,
    name="Updated Manager",
    email="updated.manager@example.com",
    permission_level="admin"
))


# =========================================================
# OPERATION TESTS
# =========================================================
print_section("OPERATION TESTS")

# These assume initial inventory already exists in the DB.
# If not, seed inventory manually in SQL before running.

pprint(client.register_sale(
    product_id=product_id_1,
    warehouse_id=warehouse_id_1,
    quantity=2
))

pprint(client.register_sale(
    product_id=product_id_2,
    warehouse_id=warehouse_id_1,
    quantity=5
))

pprint(client.transfer_stock(
    product_id=product_id_2,
    from_warehouse_id=warehouse_id_1,
    to_warehouse_id=warehouse_id_2,
    quantity=3
))


# =========================================================
# QUERY TESTS
# =========================================================
print_section("QUERY TESTS")

today = datetime.today().date()
start_date = (today - timedelta(days=90)).isoformat()
end_date = today.isoformat()

year = today.year
month = today.month

pprint(client.get_product_stock(product_id_1))
pprint(client.get_low_stock(threshold=10))
pprint(client.get_inventory_by_warehouse(warehouse_id_1))
pprint(client.search_products("Laptop"))
pprint(client.search_products_advanced("wireless"))

pprint(client.get_stock_movements(
    product_id=product_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_net_stock_change(
    product_id=product_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_stock_trend(product_id_1))

pprint(client.get_total_sales(
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_top_products(
    limit_n=5,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_slow_moving_products(days=30))

pprint(client.get_inventory_turnover(
    product_id=product_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_days_of_inventory(product_id_1))
pprint(client.estimate_demand(product_id_1, window_days=30))

pprint(client.get_category_sales(
    category_id=category_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_category_stock(category_id_1))

pprint(client.get_top_categories(
    limit_n=5,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_categories_without_sales(
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_monthly_sales_summary(
    year=year,
    month=month
))

pprint(client.get_monthly_purchase_summary(
    year=year,
    month=month
))

pprint(client.get_monthly_category_sales(
    year=year,
    month=month
))

pprint(client.get_month_over_month_growth(
    year=year,
    month=month
))

pprint(client.get_top_products_by_revenue(
    limit_n=5,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_least_sold_products(
    limit_n=5,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_warehouse_inventory_value(warehouse_id_1))
pprint(client.get_top_warehouses_by_stock())

pprint(client.get_warehouse_low_stock_products(
    warehouse_id=warehouse_id_1,
    threshold=5
))

pprint(client.get_supplier_spend(
    supplier_id=supplier_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_top_suppliers(
    limit_n=5,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_out_of_stock_products())

pprint(client.get_products_needing_restock(
    days_window=30,
    min_days_remaining=7.0
))

pprint(client.get_products_without_recent_sales(days=30))

pprint(client.get_daily_revenue(
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_daily_product_sales(
    product_id=product_id_1,
    start_date=start_date,
    end_date=end_date
))

pprint(client.get_monthly_revenue_by_category(year=year))


# =========================================================
# LOOKUP TESTS
# =========================================================
print_section("LOOKUP TESTS")

pprint(client.get_all_categories())
pprint(client.get_all_products())
pprint(client.get_all_warehouses())
pprint(client.get_all_suppliers())
pprint(client.get_all_users())

# =========================================================
# LOGOUT
# =========================================================
print_section("LOGOUT")

logout_result = client.logout()
pprint(logout_result)

print("\nAll tests completed successfully.")