from fastapi import APIRouter, HTTPException, Query, Response, Request
from api.db.interface import get_connection, run_proc
from api.routes.sessions import validate_request
from typing import Optional

router = APIRouter(prefix="/queries", tags=["queries"])


@router.get("/product-stock/{product_id}")
def get_product_stock(request: Request, product_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_product_stock",
            args=(product_id,)
        )

        return {
            "warehouses": result[0] if len(result) > 0 else [],
            "total_stock": result[1][0]["total_stock"] if len(result) > 1 and len(result[1]) > 0 else 0
        }
    finally:
        conn.close()


@router.get("/low-stock")
def get_low_stock(request: Request, threshold: int = Query(..., gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_low_stock",
            args=(threshold,)
        )

        return {"items": result[0] if result else []}
    finally:
        conn.close()


@router.get("/warehouse/{warehouse_id}/inventory")
def get_inventory_by_warehouse(request: Request, warehouse_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_inventory_by_warehouse",
            args=(warehouse_id,)
        )

        return {"inventory": result[0] if result else []}
    finally:
        conn.close()


@router.get("/search-products")
def search_products(request: Request, query: str):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="search_products",
            args=(query,)
        )

        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/stock-movements")
def get_stock_movements(
    request: Request, 
    product_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_stock_movements",
            args=(product_id, start_date, end_date)
        )

        return {"movements": result[0] if result else []}
    finally:
        conn.close()


@router.get("/net-stock-change")
def get_net_stock_change(
    request: Request, 
    product_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_net_stock_change",
            args=(product_id, start_date, end_date)
        )

        return result[0][0] if result and len(result[0]) > 0 else {}
    finally:
        conn.close()


@router.get("/stock-trend/{product_id}")
def get_stock_trend(request: Request, product_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_stock_trend",
            args=(product_id,)
        )

        return {"trend": result[0] if result else []}
    finally:
        conn.close()


@router.get("/total-sales")
def get_total_sales(request: Request, start_date: str, end_date: str):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_total_sales",
            args=(start_date, end_date)
        )

        return result[0][0] if result and len(result[0]) > 0 else {"total_revenue": 0}
    finally:
        conn.close()


@router.get("/top-products")
def get_top_products(
    request: Request, 
    limit_n: int = Query(10, gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_top_products",
            args=(limit_n, start_date, end_date)
        )

        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/slow-moving-products")
def get_slow_moving_products(request: Request, days: int = Query(30, gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_slow_moving_products",
            args=(days,)
        )

        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/inventory-turnover")
def get_inventory_turnover(
    request: Request, 
    product_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_inventory_turnover",
            args=(product_id, start_date, end_date)
        )

        return result[0][0] if result and len(result[0]) > 0 else {}
    finally:
        conn.close()


@router.get("/days-of-inventory/{product_id}")
def get_days_of_inventory(request: Request, product_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_days_of_inventory",
            args=(product_id,)
        )

        return result[0][0] if result and len(result[0]) > 0 else {}
    finally:
        conn.close()


@router.get("/estimate-demand/{product_id}")
def estimate_demand(
    request: Request, 
    product_id: int,
    window_days: int = Query(30, gt=0)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="estimate_demand",
            args=(product_id, window_days)
        )

        return result[0][0] if result and len(result[0]) > 0 else {}
    finally:
        conn.close()


@router.get("/category-sales")
def get_category_sales(
    request: Request, 
    category_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_category_sales",
            args=(category_id, start_date, end_date)
        )
        return {"category_sales": result[0] if result else []}
    finally:
        conn.close()


@router.get("/category-stock/{category_id}")
def get_category_stock(request: Request, category_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_category_stock",
            args=(category_id,)
        )
        return {"stock": result[0] if result else []}
    finally:
        conn.close()


@router.get("/top-categories")
def get_top_categories(
    request: Request, 
    limit_n: int = Query(10, gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_top_categories",
            args=(limit_n, start_date, end_date)
        )
        return {"categories": result[0] if result else []}
    finally:
        conn.close()


@router.get("/categories-without-sales")
def get_categories_without_sales(request: Request, start_date: str, end_date: str):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_categories_without_sales",
            args=(start_date, end_date)
        )
        return {"categories": result[0] if result else []}
    finally:
        conn.close()


@router.get("/monthly-sales-summary")
def get_monthly_sales_summary(request: Request, year: int, month: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_monthly_sales_summary",
            args=(year, month)
        )
        return result[0][0] if result and result[0] else {}
    finally:
        conn.close()


@router.get("/monthly-purchase-summary")
def get_monthly_purchase_summary(request: Request, year: int, month: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_monthly_purchase_summary",
            args=(year, month)
        )
        return result[0][0] if result and result[0] else {}
    finally:
        conn.close()


@router.get("/monthly-category-sales")
def get_monthly_category_sales(request: Request, year: int, month: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_monthly_category_sales",
            args=(year, month)
        )
        return {"categories": result[0] if result else []}
    finally:
        conn.close()


@router.get("/month-over-month-growth")
def get_month_over_month_growth(request: Request, year: int, month: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_month_over_month_growth",
            args=(year, month)
        )
        return result[0][0] if result and result[0] else {}
    finally:
        conn.close()


@router.get("/search-products-advanced")
def search_products_advanced(request: Request, query: str):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="search_products_advanced",
            args=(query,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/top-products-by-revenue")
def get_top_products_by_revenue(
    request: Request, 
    limit_n: int = Query(10, gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_top_products_by_revenue",
            args=(limit_n, start_date, end_date)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/least-sold-products")
def get_least_sold_products(
    request: Request, 
    limit_n: int = Query(10, gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_least_sold_products",
            args=(limit_n, start_date, end_date)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/warehouse-inventory-value/{warehouse_id}")
def get_warehouse_inventory_value(request: Request, warehouse_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_warehouse_inventory_value",
            args=(warehouse_id,)
        )
        return result[0][0] if result and result[0] else {}
    finally:
        conn.close()


@router.get("/top-warehouses-by-stock")
def get_top_warehouses_by_stock(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_top_warehouses_by_stock")
        return {"warehouses": result[0] if result else []}
    finally:
        conn.close()


@router.get("/warehouse-low-stock-products")
def get_warehouse_low_stock_products(
    request: Request, 
    warehouse_id: int,
    threshold: int = Query(..., gt=0)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_warehouse_low_stock_products",
            args=(warehouse_id, threshold)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/supplier-spend")
def get_supplier_spend(
    request: Request, 
    supplier_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_supplier_spend",
            args=(supplier_id, start_date, end_date)
        )
        return result[0][0] if result and result[0] else {}
    finally:
        conn.close()


@router.get("/top-suppliers")
def get_top_suppliers(
    request: Request, 
    limit_n: int = Query(10, gt=0),
    start_date: str = Query(...),
    end_date: str = Query(...)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_top_suppliers",
            args=(limit_n, start_date, end_date)
        )
        return {"suppliers": result[0] if result else []}
    finally:
        conn.close()


@router.get("/out-of-stock-products")
def get_out_of_stock_products(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_out_of_stock_products")
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/products-needing-restock")
def get_products_needing_restock(
    request: Request, 
    days_window: int = Query(30, gt=0),
    min_days_remaining: float = Query(..., gt=0)
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_products_needing_restock",
            args=(days_window, min_days_remaining)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/products-without-recent-sales")
def get_products_without_recent_sales(request: Request, days: int = Query(30, gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_products_without_recent_sales",
            args=(days,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/daily-revenue")
def get_daily_revenue(request: Request, start_date: str, end_date: str):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_daily_revenue",
            args=(start_date, end_date)
        )
        return {"revenue": result[0] if result else []}
    finally:
        conn.close()


@router.get("/daily-product-sales")
def get_daily_product_sales(
    request: Request, 
    product_id: int,
    start_date: str,
    end_date: str
):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_daily_product_sales",
            args=(product_id, start_date, end_date)
        )
        return {"sales": result[0] if result else []}
    finally:
        conn.close()


@router.get("/monthly-revenue-by-category/{year}")
def get_monthly_revenue_by_category(request: Request, year: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_monthly_revenue_by_category",
            args=(year,)
        )
        return {"categories": result[0] if result else []}
    finally:
        conn.close()


# Generic lookup endpoints

@router.get('/lookup/categories')
def get_all_categories(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc='get_all_categories')
        return {'categories': result[0] if result else []}
    finally:
        conn.close()


@router.get('/lookup/products')
def get_all_products(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc='get_all_products')
        return {'products': result[0] if result else []}
    finally:
        conn.close()


@router.get('/lookup/warehouses')
def get_all_warehouses(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc='get_all_warehouses')
        return {'warehouses': result[0] if result else []}
    finally:
        conn.close()


@router.get('/lookup/suppliers')
def get_all_suppliers(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc='get_all_suppliers')
        return {'suppliers': result[0] if result else []}
    finally:
        conn.close()


@router.get('/lookup/users')
def get_all_users(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc='get_all_users')
        return {'users': result[0] if result else []}
    finally:
        conn.close()


@router.get("/product-lookup")
def get_product_lookup(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_product_lookup")
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/product-lookup/by-category/{category_id}")
def get_product_lookup_by_category(request: Request, category_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_product_lookup_by_category",
            args=(category_id,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/product-lookup/by-name")
def get_product_lookup_by_name(request: Request, name_query: str = Query(..., min_length=1)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_product_lookup_by_name",
            args=(name_query,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/product-lookup/by-sku")
def get_product_lookup_by_sku(request: Request, sku_query: str = Query(..., min_length=1)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_product_lookup_by_sku",
            args=(sku_query,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/category-lookup")
def get_category_lookup(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_category_lookup")
        return {"categories": result[0] if result else []}
    finally:
        conn.close()


@router.get("/warehouse-lookup")
def get_warehouse_lookup(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_warehouse_lookup")
        return {"warehouses": result[0] if result else []}
    finally:
        conn.close()


@router.get("/warehouse-products/{warehouse_id}")
def get_warehouse_products(request: Request, warehouse_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_warehouse_products",
            args=(warehouse_id,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/supplier-lookup")
def get_supplier_lookup(request: Request):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(conn=conn, proc="get_supplier_lookup")
        return {"suppliers": result[0] if result else []}
    finally:
        conn.close()


@router.get("/supplier-products/{supplier_id}")
def get_supplier_products(request: Request, supplier_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_supplier_products",
            args=(supplier_id,)
        )
        return {"products": result[0] if result else []}
    finally:
        conn.close()


@router.get("/sales-lookup")
def get_sales_lookup(request: Request, limit_n: int = Query(50, gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_sales_lookup",
            args=(limit_n,)
        )
        return {"sales": result[0] if result else []}
    finally:
        conn.close()


@router.get("/sale-details/{sale_id}")
def get_sale_details(request: Request, sale_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_sale_details",
            args=(sale_id,)
        )
        return {"details": result[0] if result else []}
    finally:
        conn.close()


@router.get("/purchases-lookup")
def get_purchases_lookup(request: Request, limit_n: int = Query(50, gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_purchases_lookup",
            args=(limit_n,)
        )
        return {"purchases": result[0] if result else []}
    finally:
        conn.close()


@router.get("/purchase-details/{purchase_id}")
def get_purchase_details(request: Request, purchase_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_purchase_details",
            args=(purchase_id,)
        )
        return {"details": result[0] if result else []}
    finally:
        conn.close()


@router.get("/recent-stock-movements")
def get_recent_stock_movements(request: Request, limit_n: int = Query(50, gt=0)):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_recent_stock_movements",
            args=(limit_n,)
        )
        return {"movements": result[0] if result else []}
    finally:
        conn.close()


@router.get("/product-movement-lookup/{product_id}")
def get_product_movement_lookup(request: Request, product_id: int):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="get_product_movement_lookup",
            args=(product_id,)
        )
        return {"movements": result[0] if result else []}
    finally:
        conn.close()