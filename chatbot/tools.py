from typing import Any
from langchain.tools import tool

from chatbot.session import CLIENT, safe_api_call


@tool(description="Retrieve stock levels for a specific product across all warehouses, including per-warehouse quantities and total stock.")
@safe_api_call
def get_product_stock(product_id: int) -> dict[str, Any]:
    return CLIENT.get_product_stock(product_id=product_id)


@tool(description="Retrieve products whose total stock is below a specified threshold.")
@safe_api_call
def get_low_stock(threshold: int) -> dict[str, Any]:
    return CLIENT.get_low_stock(threshold=threshold)


@tool(description="Retrieve all products and their quantities stored in a specific warehouse.")
@safe_api_call
def get_inventory_by_warehouse(warehouse_id: int) -> dict[str, Any]:
    return CLIENT.get_inventory_by_warehouse(warehouse_id=warehouse_id)


@tool(description="Search for products by name or SKU using a partial text query.")
@safe_api_call
def search_products(query: str) -> dict[str, Any]:
    return CLIENT.search_products(query=query)


@tool(description="Retrieve stock movement records for a product within a date range.")
@safe_api_call
def get_stock_movements(
    product_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_stock_movements(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Calculate total incoming stock, outgoing stock, and net stock change for a product within a date range.")
@safe_api_call
def get_net_stock_change(
    product_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_net_stock_change(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve the daily stock movement trend for a product over time.")
@safe_api_call
def get_stock_trend(product_id: int) -> dict[str, Any]:
    return CLIENT.get_stock_trend(product_id=product_id)


@tool(description="Calculate total sales revenue within a specified date range.")
@safe_api_call
def get_total_sales(start_date: str, end_date: str) -> dict[str, Any]:
    return CLIENT.get_total_sales(
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve the top-selling products by units sold within a specified date range.")
@safe_api_call
def get_top_products(
    limit_n: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_top_products(
        limit_n=limit_n,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve products with no sales during the last specified number of days.")
@safe_api_call
def get_slow_moving_products(days: int) -> dict[str, Any]:
    return CLIENT.get_slow_moving_products(days=days)


@tool(description="Calculate the inventory turnover ratio for a product within a specified date range.")
@safe_api_call
def get_inventory_turnover(
    product_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_inventory_turnover(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Estimate how many days current inventory for a product will last based on recent sales.")
@safe_api_call
def get_days_of_inventory(product_id: int) -> dict[str, Any]:
    return CLIENT.get_days_of_inventory(product_id=product_id)


@tool(description="Estimate average daily demand for a product over a specified time window.")
@safe_api_call
def estimate_demand(product_id: int, window_days: int) -> dict[str, Any]:
    return CLIENT.estimate_demand(
        product_id=product_id,
        window_days=window_days
    )


@tool(description="Transfer stock of a product from one warehouse to another and record the corresponding stock movements.")
@safe_api_call
def transfer_stock(
    product_id: int,
    from_warehouse_id: int,
    to_warehouse_id: int,
    quantity: int
) -> dict[str, Any]:
    return CLIENT.transfer_stock(
        product_id=product_id,
        from_warehouse_id=from_warehouse_id,
        to_warehouse_id=to_warehouse_id,
        quantity=quantity
    )


@tool(description="Create a new user with name, email, password, and permission level.")
@safe_api_call
def create_user(
    name: str,
    email: str,
    password: str,
    permission_level: str
) -> dict[str, Any]:
    return CLIENT.create_user(
        name=name,
        email=email,
        password=password,
        permission_level=permission_level
    )


@tool(description="Retrieve sales performance metrics for a category, including units sold and revenue within a date range.")
@safe_api_call
def get_category_sales(
    category_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_category_sales(
        category_id=category_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve stock information for all products within a category.")
@safe_api_call
def get_category_stock(category_id: int) -> dict[str, Any]:
    return CLIENT.get_category_stock(category_id=category_id)


@tool(description="Retrieve the top-performing categories by revenue within a specified date range.")
@safe_api_call
def get_top_categories(
    limit_n: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_top_categories(
        limit_n=limit_n,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve categories with no sales during a specified date range.")
@safe_api_call
def get_categories_without_sales(
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_categories_without_sales(
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve a summary of total sales, units sold, and revenue for a specific month.")
@safe_api_call
def get_monthly_sales_summary(year: int, month: int) -> dict[str, Any]:
    return CLIENT.get_monthly_sales_summary(year=year, month=month)


@tool(description="Retrieve a summary of total purchases, units purchased, and spending for a specific month.")
@safe_api_call
def get_monthly_purchase_summary(year: int, month: int) -> dict[str, Any]:
    return CLIENT.get_monthly_purchase_summary(year=year, month=month)


@tool(description="Retrieve category-level sales performance for a specific month.")
@safe_api_call
def get_monthly_category_sales(year: int, month: int) -> dict[str, Any]:
    return CLIENT.get_monthly_category_sales(year=year, month=month)


@tool(description="Calculate revenue growth percentage between a month and the previous month.")
@safe_api_call
def get_month_over_month_growth(year: int, month: int) -> dict[str, Any]:
    return CLIENT.get_month_over_month_growth(year=year, month=month)


@tool(description="Search for products using name, description, SKU, or category name.")
@safe_api_call
def search_products_advanced(query: str) -> dict[str, Any]:
    return CLIENT.search_products_advanced(query=query)


@tool(description="Retrieve the top products ranked by total revenue within a specified date range.")
@safe_api_call
def get_top_products_by_revenue(
    limit_n: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_top_products_by_revenue(
        limit_n=limit_n,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve the least sold products within a specified date range.")
@safe_api_call
def get_least_sold_products(
    limit_n: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_least_sold_products(
        limit_n=limit_n,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Calculate the total inventory value stored in a specific warehouse.")
@safe_api_call
def get_warehouse_inventory_value(warehouse_id: int) -> dict[str, Any]:
    return CLIENT.get_warehouse_inventory_value(warehouse_id=warehouse_id)


@tool(description="Retrieve warehouses ranked by total stock quantity.")
@safe_api_call
def get_top_warehouses_by_stock() -> dict[str, Any]:
    return CLIENT.get_top_warehouses_by_stock()


@tool(description="Retrieve products in a warehouse whose stock is below a specified threshold.")
@safe_api_call
def get_warehouse_low_stock_products(
    warehouse_id: int,
    threshold: int
) -> dict[str, Any]:
    return CLIENT.get_warehouse_low_stock_products(
        warehouse_id=warehouse_id,
        threshold=threshold
    )


@tool(description="Retrieve the total amount spent with a supplier within a specified date range.")
@safe_api_call
def get_supplier_spend(
    supplier_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_supplier_spend(
        supplier_id=supplier_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve the suppliers with the highest total spending within a specified date range.")
@safe_api_call
def get_top_suppliers(
    limit_n: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_top_suppliers(
        limit_n=limit_n,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve products that currently have no stock available.")
@safe_api_call
def get_out_of_stock_products() -> dict[str, Any]:
    return CLIENT.get_out_of_stock_products()


@tool(description="Retrieve products likely to require restocking soon based on stock levels and recent sales.")
@safe_api_call
def get_products_needing_restock(
    days_window: int,
    min_days_remaining: float
) -> dict[str, Any]:
    return CLIENT.get_products_needing_restock(
        days_window=days_window,
        min_days_remaining=min_days_remaining
    )


@tool(description="Retrieve products that have not had any recent sales within a specified number of days.")
@safe_api_call
def get_products_without_recent_sales(days: int) -> dict[str, Any]:
    return CLIENT.get_products_without_recent_sales(days=days)


@tool(description="Retrieve daily revenue values within a specified date range.")
@safe_api_call
def get_daily_revenue(start_date: str, end_date: str) -> dict[str, Any]:
    return CLIENT.get_daily_revenue(
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve daily sales quantities for a specific product within a specified date range.")
@safe_api_call
def get_daily_product_sales(
    product_id: int,
    start_date: str,
    end_date: str
) -> dict[str, Any]:
    return CLIENT.get_daily_product_sales(
        product_id=product_id,
        start_date=start_date,
        end_date=end_date
    )


@tool(description="Retrieve monthly revenue grouped by category for a given year.")
@safe_api_call
def get_monthly_revenue_by_category(year: int) -> dict[str, Any]:
    return CLIENT.get_monthly_revenue_by_category(year=year)


@tool(description="Retrieve a list of all categories.")
@safe_api_call
def get_all_categories() -> dict[str, Any]:
    return CLIENT.get_all_categories()


@tool(description="Retrieve a list of all products with category, SKU, price, and creation date.")
@safe_api_call
def get_all_products() -> dict[str, Any]:
    return CLIENT.get_all_products()


@tool(description="Retrieve a list of all warehouses and their locations.")
@safe_api_call
def get_all_warehouses() -> dict[str, Any]:
    return CLIENT.get_all_warehouses()


@tool(description="Retrieve a list of all suppliers and their contact information.")
@safe_api_call
def get_all_suppliers() -> dict[str, Any]:
    return CLIENT.get_all_suppliers()


@tool(description="Retrieve a list of all users and their permission levels.")
@safe_api_call
def get_all_users() -> dict[str, Any]:
    return CLIENT.get_all_users()


@tool(description="Create a new category and return its generated category ID.")
@safe_api_call
def create_category(name: str) -> dict[str, Any]:
    return CLIENT.create_category(name=name)

@tool(description="Update the name of an existing category.")
@safe_api_call
def update_category(
    category_id: int,
    name: str
) -> dict[str, Any]:
    return CLIENT.update_category(
        category_id=category_id,
        name=name
    )


@tool(description="Create a new product with name, description, SKU, category, and unit price.")
@safe_api_call
def create_product(
    name: str,
    description: str,
    sku: str,
    category_id: int,
    unit_price: float
) -> dict[str, Any]:
    return CLIENT.create_product(
        name=name,
        description=description,
        sku=sku,
        category_id=category_id,
        unit_price=unit_price
    )


@tool(description="Update the information of an existing product.")
@safe_api_call
def update_product(
    product_id: int,
    name: str,
    description: str,
    sku: str,
    category_id: int,
    unit_price: float
) -> dict[str, Any]:
    return CLIENT.update_product(
        product_id=product_id,
        name=name,
        description=description,
        sku=sku,
        category_id=category_id,
        unit_price=unit_price
    )


@tool(description="Create a new warehouse with a name and location.")
@safe_api_call
def create_warehouse(
    name: str,
    location: str
) -> dict[str, Any]:
    return CLIENT.create_warehouse(
        name=name,
        location=location
    )


@tool(description="Update the information of an existing warehouse.")
@safe_api_call
def update_warehouse(
    warehouse_id: int,
    name: str,
    location: str
) -> dict[str, Any]:
    return CLIENT.update_warehouse(
        warehouse_id=warehouse_id,
        name=name,
        location=location
    )


@tool(description="Create a new supplier with a name and contact information.")
@safe_api_call
def create_supplier(
    name: str,
    contact_info: str
) -> dict[str, Any]:
    return CLIENT.create_supplier(
        name=name,
        contact_info=contact_info
    )


@tool(description="Update the information of an existing supplier.")
@safe_api_call
def update_supplier(
    supplier_id: int,
    name: str,
    contact_info: str
) -> dict[str, Any]:
    return CLIENT.update_supplier(
        supplier_id=supplier_id,
        name=name,
        contact_info=contact_info
    )


@tool(description="Create a new user with name, email, password, and permission level.")
@safe_api_call
def create_user(
    name: str,
    email: str,
    password: str,
    permission_level: str
) -> dict[str, Any]:
    return CLIENT.create_user(
        name=name,
        email=email,
        password=password,
        permission_level=permission_level
    )


@tool(description="Update the name, email, and permission level of an existing user.")
@safe_api_call
def update_user(
    user_id: int,
    name: str,
    email: str,
    permission_level: str
) -> dict[str, Any]:
    return CLIENT.update_user(
        user_id=user_id,
        name=name,
        email=email,
        permission_level=permission_level
    )


@tool(description="Create a new purchase for a supplier and return a temporary purchase session key.")
@safe_api_call
def create_purchase(
    supplier_id: int
) -> dict[str, Any]:
    return CLIENT.create_purchase(
        supplier_id=supplier_id
    )


@tool(description="Add a product item to an existing purchase session.")
@safe_api_call
def add_purchase_item(
    purchase_session_key: str,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    price: float
) -> dict[str, Any]:
    return CLIENT.add_purchase_item(
        purchase_session_key=purchase_session_key,
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
        price=price
    )


@tool(description="Close a purchase session so no more items can be added.")
@safe_api_call
def close_purchase(
    purchase_session_key: str
) -> dict[str, Any]:
    return CLIENT.close_purchase(
        purchase_session_key=purchase_session_key
    )


@tool(description="Create a new sale and return a temporary sale session key.")
@safe_api_call
def create_sale() -> dict[str, Any]:
    return CLIENT.create_sale()


@tool(description="Add a product item to an existing sale session.")
@safe_api_call
def add_sale_item(
    sale_session_key: str,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    price: float
) -> dict[str, Any]:
    return CLIENT.add_sale_item(
        sale_session_key=sale_session_key,
        product_id=product_id,
        warehouse_id=warehouse_id,
        quantity=quantity,
        price=price
    )