import requests
from typing import Any


class APIClient:
    def __init__(
        self,
        base_url: str = "http://localhost:8000"
    ):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()


    def login(self, username: str, password: str) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/auth/login",
            params={
                "username": username,
                "password": password
            }
        )

        response.raise_for_status()
        return response.json()


    def logout(self) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/auth/logout"
        )

        response.raise_for_status()
        return response.json()


    def me(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/auth/me"
        )

        response.raise_for_status()
        return response.json()


    def get_product_stock(self, product_id: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/product-stock/{product_id}"
        )

        response.raise_for_status()
        return response.json()


    def get_low_stock(self, threshold: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/low-stock",
            params={"threshold": threshold}
        )

        response.raise_for_status()
        return response.json()


    def get_inventory_by_warehouse(self, warehouse_id: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/warehouse/{warehouse_id}/inventory"
        )

        response.raise_for_status()
        return response.json()


    def search_products(self, query: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/search-products",
            params={"query": query}
        )

        response.raise_for_status()
        return response.json()


    def get_stock_movements(
        self,
        product_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/stock-movements",
            params={
                "product_id": product_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_net_stock_change(
        self,
        product_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/net-stock-change",
            params={
                "product_id": product_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_stock_trend(self, product_id: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/stock-trend/{product_id}"
        )

        response.raise_for_status()
        return response.json()


    def get_total_sales(self, start_date: str, end_date: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/total-sales",
            params={
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_top_products(
        self,
        limit_n: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/top-products",
            params={
                "limit_n": limit_n,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_slow_moving_products(self, days: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/slow-moving-products",
            params={"days": days}
        )

        response.raise_for_status()
        return response.json()


    def get_inventory_turnover(
        self,
        product_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/inventory-turnover",
            params={
                "product_id": product_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_days_of_inventory(self, product_id: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/days-of-inventory/{product_id}"
        )

        response.raise_for_status()
        return response.json()


    def estimate_demand(self, product_id: int, window_days: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/estimate-demand/{product_id}",
            params={"window_days": window_days}
        )

        response.raise_for_status()
        return response.json()
    

    def transfer_stock(
        self,
        product_id: int,
        from_warehouse_id: int,
        to_warehouse_id: int,
        quantity: int
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/transfer-stock",
            json={
                "product_id": product_id,
                "from_warehouse_id": from_warehouse_id,
                "to_warehouse_id": to_warehouse_id,
                "quantity": quantity
            }
        )

        response.raise_for_status()
        return response.json()


    def create_user(
        self,
        name: str,
        email: str,
        password: str,
        permission_level: str
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-user",
            json={
                "name": name,
                "email": email,
                "password": password,
                "permission_level": permission_level
            }
        )

        response.raise_for_status()
        return response.json()
    

    def get_category_sales(
        self,
        category_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/category-sales",
            params={
                "category_id": category_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_category_stock(self, category_id: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/category-stock/{category_id}"
        )

        response.raise_for_status()
        return response.json()


    def get_top_categories(
        self,
        limit_n: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/top-categories",
            params={
                "limit_n": limit_n,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_categories_without_sales(
        self,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/categories-without-sales",
            params={
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_monthly_sales_summary(
        self,
        year: int,
        month: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/monthly-sales-summary",
            params={
                "year": year,
                "month": month
            }
        )

        response.raise_for_status()
        return response.json()


    def get_monthly_purchase_summary(
        self,
        year: int,
        month: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/monthly-purchase-summary",
            params={
                "year": year,
                "month": month
            }
        )

        response.raise_for_status()
        return response.json()


    def get_monthly_category_sales(
        self,
        year: int,
        month: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/monthly-category-sales",
            params={
                "year": year,
                "month": month
            }
        )

        response.raise_for_status()
        return response.json()


    def get_month_over_month_growth(
        self,
        year: int,
        month: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/month-over-month-growth",
            params={
                "year": year,
                "month": month
            }
        )

        response.raise_for_status()
        return response.json()


    def search_products_advanced(self, query: str) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/search-products-advanced",
            params={"query": query}
        )

        response.raise_for_status()
        return response.json()


    def get_top_products_by_revenue(
        self,
        limit_n: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/top-products-by-revenue",
            params={
                "limit_n": limit_n,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_least_sold_products(
        self,
        limit_n: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/least-sold-products",
            params={
                "limit_n": limit_n,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_warehouse_inventory_value(
        self,
        warehouse_id: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/warehouse-inventory-value/{warehouse_id}"
        )

        response.raise_for_status()
        return response.json()


    def get_top_warehouses_by_stock(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/top-warehouses-by-stock"
        )

        response.raise_for_status()
        return response.json()


    def get_warehouse_low_stock_products(
        self,
        warehouse_id: int,
        threshold: int
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/warehouse-low-stock-products",
            params={
                "warehouse_id": warehouse_id,
                "threshold": threshold
            }
        )

        response.raise_for_status()
        return response.json()


    def get_supplier_spend(
        self,
        supplier_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/supplier-spend",
            params={
                "supplier_id": supplier_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_top_suppliers(
        self,
        limit_n: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/top-suppliers",
            params={
                "limit_n": limit_n,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_out_of_stock_products(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/out-of-stock-products"
        )

        response.raise_for_status()
        return response.json()


    def get_products_needing_restock(
        self,
        days_window: int,
        min_days_remaining: float
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/products-needing-restock",
            params={
                "days_window": days_window,
                "min_days_remaining": min_days_remaining
            }
        )

        response.raise_for_status()
        return response.json()


    def get_products_without_recent_sales(self, days: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/products-without-recent-sales",
            params={"days": days}
        )

        response.raise_for_status()
        return response.json()


    def get_daily_revenue(
        self,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/daily-revenue",
            params={
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_daily_product_sales(
        self,
        product_id: int,
        start_date: str,
        end_date: str
    ) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/daily-product-sales",
            params={
                "product_id": product_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        response.raise_for_status()
        return response.json()


    def get_monthly_revenue_by_category(self, year: int) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/monthly-revenue-by-category/{year}"
        )

        response.raise_for_status()
        return response.json()


    def get_all_categories(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/lookup/categories"
        )

        response.raise_for_status()
        return response.json()


    def get_all_products(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/lookup/products"
        )

        response.raise_for_status()
        return response.json()


    def get_all_warehouses(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/lookup/warehouses"
        )

        response.raise_for_status()
        return response.json()


    def get_all_suppliers(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/lookup/suppliers"
        )

        response.raise_for_status()
        return response.json()


    def get_all_users(self) -> dict[str, Any]:
        response = self.session.get(
            f"{self.base_url}/queries/lookup/users"
        )

        response.raise_for_status()
        return response.json()


    def create_category(self, name: str) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-category",
            json={
                "name": name
            }
        )

        response.raise_for_status()
        return response.json()


    def update_category(
        self,
        category_id: int,
        name: str
    ) -> dict[str, Any]:
        response = self.session.put(
            f"{self.base_url}/operations/update-category",
            json={
                "category_id": category_id,
                "name": name
            }
        )

        response.raise_for_status()
        return response.json()


    def create_product(
        self,
        name: str,
        description: str,
        sku: str,
        category_id: int,
        unit_price: float
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-product",
            json={
                "name": name,
                "description": description,
                "sku": sku,
                "category_id": category_id,
                "unit_price": unit_price
            }
        )

        response.raise_for_status()
        return response.json()


    def update_product(
        self,
        product_id: int,
        name: str,
        description: str,
        sku: str,
        category_id: int,
        unit_price: float
    ) -> dict[str, Any]:
        response = self.session.put(
            f"{self.base_url}/operations/update-product",
            json={
                "product_id": product_id,
                "name": name,
                "description": description,
                "sku": sku,
                "category_id": category_id,
                "unit_price": unit_price
            }
        )

        response.raise_for_status()
        return response.json()


    def create_warehouse(
        self,
        name: str,
        location: str
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-warehouse",
            json={
                "name": name,
                "location": location
            }
        )

        response.raise_for_status()
        return response.json()


    def update_warehouse(
        self,
        warehouse_id: int,
        name: str,
        location: str
    ) -> dict[str, Any]:
        response = self.session.put(
            f"{self.base_url}/operations/update-warehouse",
            json={
                "warehouse_id": warehouse_id,
                "name": name,
                "location": location
            }
        )

        response.raise_for_status()
        return response.json()


    def create_supplier(
        self,
        name: str,
        contact_info: str
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-supplier",
            json={
                "name": name,
                "contact_info": contact_info
            }
        )

        response.raise_for_status()
        return response.json()


    def update_supplier(
        self,
        supplier_id: int,
        name: str,
        contact_info: str
    ) -> dict[str, Any]:
        response = self.session.put(
            f"{self.base_url}/operations/update-supplier",
            json={
                "supplier_id": supplier_id,
                "name": name,
                "contact_info": contact_info
            }
        )

        response.raise_for_status()
        return response.json()
    

    def update_user(
        self,
        user_id: int,
        name: str,
        email: str,
        permission_level: str
    ) -> dict[str, Any]:
        response = self.session.put(
            f"{self.base_url}/operations/update-user",
            json={
                "user_id": user_id,
                "name": name,
                "email": email,
                "permission_level": permission_level
            }
        )

        response.raise_for_status()
        return response.json()
    

    def create_purchase(
        self,
        supplier_id: int
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-purchase",
            json={
                "supplier_id": supplier_id
            }
        )

        response.raise_for_status()
        return response.json()


    def add_purchase_item(
        self,
        purchase_session_key: str,
        product_id: int,
        warehouse_id: int,
        quantity: int,
        price: float
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/add-purchase-item",
            json={
                "purchase_session_key": purchase_session_key,
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "quantity": quantity,
                "price": price
            }
        )

        response.raise_for_status()
        return response.json()


    def create_sale(
        self
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/create-sale"
        )

        response.raise_for_status()
        return response.json()


    def add_sale_item(
        self,
        sale_session_key: str,
        product_id: int,
        warehouse_id: int,
        quantity: int,
        price: float
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/add-sale-item",
            json={
                "sale_session_key": sale_session_key,
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "quantity": quantity,
                "price": price
            }
        )

        response.raise_for_status()
        return response.json()


    def close_purchase(
        self,
        purchase_session_key: str
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/close-purchase",
            json={
                "purchase_session_key": purchase_session_key
            }
        )

        response.raise_for_status()
        return response.json()


    def close_sale(
        self,
        sale_session_key: str
    ) -> dict[str, Any]:
        response = self.session.post(
            f"{self.base_url}/operations/close-sale",
            json={
                "sale_session_key": sale_session_key
            }
        )

        response.raise_for_status()
        return response.json()
    
    