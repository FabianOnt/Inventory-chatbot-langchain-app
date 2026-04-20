CREATE PROCEDURE get_product_stock(
    IN p_product_id INT
)
BEGIN
    SELECT 
        w.warehouse_id,
        w.name AS warehouse_name,
        s.quantity
    FROM stock s
    JOIN warehouses w ON s.warehouse_id = w.warehouse_id
    WHERE s.product_id = p_product_id;

    SELECT SUM(quantity) AS total_stock
    FROM stock
    WHERE product_id = p_product_id;
END //


CREATE PROCEDURE get_low_stock(
    IN threshold INT
)
BEGIN
    SELECT p.product_id, p.name, SUM(s.quantity) AS total_stock
    FROM products p
    JOIN stock s ON p.product_id = s.product_id
    GROUP BY p.product_id
    HAVING total_stock < threshold;
END //


CREATE PROCEDURE get_inventory_by_warehouse(
    IN p_warehouse_id INT
)
BEGIN
    SELECT p.product_id, p.name, s.quantity
    FROM stock s
    JOIN products p ON s.product_id = p.product_id
    WHERE s.warehouse_id = p_warehouse_id;
END //


CREATE PROCEDURE search_products(
    IN query VARCHAR(255)
)
BEGIN
    SELECT *
    FROM products
    WHERE name LIKE CONCAT('%', query, '%')
       OR sku LIKE CONCAT('%', query, '%');
END //


CREATE PROCEDURE get_stock_movements(
    IN p_product_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT *
    FROM stock_movements
    WHERE product_id = p_product_id
      AND created_at BETWEEN start_date AND end_date
    ORDER BY created_at;
END //


CREATE PROCEDURE get_net_stock_change(
    IN p_product_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT 
        SUM(CASE WHEN movement_type = 'IN' THEN quantity ELSE 0 END) AS total_in,
        SUM(CASE WHEN movement_type = 'OUT' THEN quantity ELSE 0 END) AS total_out,
        SUM(CASE 
            WHEN movement_type = 'IN' THEN quantity 
            ELSE -quantity 
        END) AS net_change
    FROM stock_movements
    WHERE product_id = p_product_id
      AND created_at BETWEEN start_date AND end_date;
END //


CREATE PROCEDURE get_stock_trend(
    IN p_product_id INT
)
BEGIN
    SELECT 
        DATE(created_at) AS day,
        SUM(CASE 
            WHEN movement_type = 'IN' THEN quantity
            ELSE -quantity
        END) AS net
    FROM stock_movements
    WHERE product_id = p_product_id
    GROUP BY day
    ORDER BY day;
END //


CREATE PROCEDURE get_total_sales(
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT 
        SUM(quantity * price) AS total_revenue
    FROM sale_items
    JOIN sales USING (sale_id)
    WHERE created_at BETWEEN start_date AND end_date;
END //


CREATE PROCEDURE get_top_products(
    IN limit_n INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT 
        p.product_id,
        p.name,
        SUM(si.quantity) AS total_sold
    FROM sale_items si
    JOIN sales s USING (sale_id)
    JOIN products p ON si.product_id = p.product_id
    WHERE s.created_at BETWEEN start_date AND end_date
    GROUP BY p.product_id
    ORDER BY total_sold DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_slow_moving_products(
    IN days INT
)
BEGIN
    SELECT p.product_id, p.name, IFNULL(SUM(h.quantity), 0) AS total_sold
    FROM products p
    LEFT JOIN 
        (
            SELECT * FROM sale_items si
            JOIN sales s USING (sale_id)
            WHERE s.created_at >= NOW() - INTERVAL days DAY
        ) AS h
        ON p.product_id = h.product_id
    GROUP BY p.product_id
    HAVING total_sold = 0;
END //


CREATE PROCEDURE get_inventory_turnover(
    IN p_product_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    DECLARE total_sales INT;
    DECLARE avg_stock FLOAT;

    SELECT SUM(quantity) INTO total_sales
    FROM sale_items
    JOIN sales USING (sale_id)
    WHERE product_id = p_product_id
      AND created_at BETWEEN start_date AND end_date;

    SELECT AVG(quantity) INTO avg_stock
    FROM stock
    WHERE product_id = p_product_id;

    SELECT total_sales / NULLIF(avg_stock, 0) AS turnover_ratio;
END //


CREATE PROCEDURE get_days_of_inventory(
    IN p_product_id INT
)
BEGIN
    DECLARE daily_sales FLOAT;
    DECLARE current_stock INT;

    SELECT AVG(quantity) INTO daily_sales
    FROM sale_items
    JOIN sales USING (sale_id)
    WHERE product_id = p_product_id
      AND created_at >= NOW() - INTERVAL 30 DAY;

    SELECT SUM(quantity) INTO current_stock
    FROM stock
    WHERE product_id = p_product_id;

    SELECT current_stock / NULLIF(daily_sales, 0) AS days_remaining;
END //


CREATE PROCEDURE estimate_demand(
    IN p_product_id INT,
    IN window_days INT
)
BEGIN
    SELECT AVG(quantity) AS avg_daily_demand
    FROM sale_items
    JOIN sales USING (sale_id)
    WHERE product_id = p_product_id
      AND created_at >= NOW() - INTERVAL window_days DAY;
END //


CREATE PROCEDURE register_sale(
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_quantity INT
)
BEGIN
    UPDATE stock
    SET quantity = quantity - p_quantity
    WHERE product_id = p_product_id
      AND warehouse_id = p_warehouse_id;

    INSERT INTO stock_movements (product_id, warehouse_id, quantity, movement_type)
    VALUES (p_product_id, p_warehouse_id, p_quantity, 'OUT');
END //


CREATE PROCEDURE transfer_stock(
    IN p_product_id INT,
    IN from_wh INT,
    IN to_wh INT,
    IN qty INT
)
BEGIN
    UPDATE stock
    SET quantity = quantity - qty
    WHERE product_id = p_product_id AND warehouse_id = from_wh;

    INSERT INTO stock (product_id, warehouse_id, quantity)
    VALUES (p_product_id, to_wh, qty)
    ON DUPLICATE KEY UPDATE quantity = quantity + qty;

    INSERT INTO stock_movements VALUES (NULL, p_product_id, from_wh, qty, 'OUT', NULL, NOW());
    INSERT INTO stock_movements VALUES (NULL, p_product_id, to_wh, qty, 'IN', NULL, NOW());
END //


CREATE PROCEDURE request_session (
    IN p_email VARCHAR(255)
)
BEGIN
    SELECT
        u.email,
        u.password,
        u.permission_level
    FROM users u
    WHERE u.email = p_email;
END //


CREATE PROCEDURE get_category_sales(
    IN p_category_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        c.category_id,
        c.name AS category_name,
        SUM(si.quantity) AS total_units_sold,
        SUM(si.quantity * si.price) AS total_revenue
    FROM sale_items si
    JOIN products p ON si.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    JOIN sales s ON si.sale_id = s.sale_id
    WHERE c.category_id = p_category_id
      AND s.created_at BETWEEN start_date AND end_date
    GROUP BY c.category_id, c.name;
END //


CREATE PROCEDURE get_category_stock(
    IN p_category_id INT
)
BEGIN
    SELECT
        c.category_id,
        c.name AS category_name,
        p.product_id,
        p.name AS product_name,
        SUM(s.quantity) AS total_stock
    FROM stock s
    JOIN products p ON s.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    WHERE c.category_id = p_category_id
    GROUP BY c.category_id, c.name, p.product_id, p.name
    ORDER BY total_stock DESC;
END //


CREATE PROCEDURE get_top_categories(
    IN limit_n INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        c.category_id,
        c.name AS category_name,
        SUM(si.quantity) AS total_units_sold,
        SUM(si.quantity * si.price) AS total_revenue
    FROM sale_items si
    JOIN products p ON si.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    JOIN sales s ON si.sale_id = s.sale_id
    WHERE s.created_at BETWEEN start_date AND end_date
    GROUP BY c.category_id, c.name
    ORDER BY total_revenue DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_categories_without_sales(
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        c.category_id,
        c.name AS category_name
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
    LEFT JOIN sale_items si ON p.product_id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.sale_id
        AND s.created_at BETWEEN start_date AND end_date
    GROUP BY c.category_id, c.name
    HAVING SUM(CASE WHEN s.sale_id IS NOT NULL THEN 1 ELSE 0 END) = 0;
END //


CREATE PROCEDURE get_monthly_sales_summary(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT
        COUNT(DISTINCT s.sale_id) AS total_sales,
        SUM(si.quantity) AS total_units_sold,
        SUM(si.quantity * si.price) AS total_revenue
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    WHERE YEAR(s.created_at) = p_year
      AND MONTH(s.created_at) = p_month;
END //


CREATE PROCEDURE get_monthly_purchase_summary(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT
        COUNT(DISTINCT p.purchase_id) AS total_purchases,
        SUM(pi.quantity) AS total_units_purchased,
        SUM(pi.quantity * pi.price) AS total_spend
    FROM purchases p
    JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    WHERE YEAR(p.created_at) = p_year
      AND MONTH(p.created_at) = p_month;
END //


CREATE PROCEDURE get_monthly_category_sales(
    IN p_year INT,
    IN p_month INT
)
BEGIN
    SELECT
        c.category_id,
        c.name AS category_name,
        SUM(si.quantity) AS total_units_sold,
        SUM(si.quantity * si.price) AS total_revenue
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    JOIN products p ON si.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    WHERE YEAR(s.created_at) = p_year
      AND MONTH(s.created_at) = p_month
    GROUP BY c.category_id, c.name
    ORDER BY total_revenue DESC;
END //


CREATE PROCEDURE get_month_over_month_growth(
    IN current_year INT,
    IN current_month INT
)
BEGIN
    DECLARE prev_year INT;
    DECLARE prev_month INT;

    IF current_month = 1 THEN
        SET prev_month = 12;
        SET prev_year = current_year - 1;
    ELSE
        SET prev_month = current_month - 1;
        SET prev_year = current_year;
    END IF;

    SELECT
        current_data.total_revenue AS current_month_revenue,
        previous_data.total_revenue AS previous_month_revenue,
        (
            (current_data.total_revenue - previous_data.total_revenue)
            / NULLIF(previous_data.total_revenue, 0)
        ) * 100 AS growth_percentage
    FROM
    (
        SELECT SUM(si.quantity * si.price) AS total_revenue
        FROM sales s
        JOIN sale_items si ON s.sale_id = si.sale_id
        WHERE YEAR(s.created_at) = current_year
          AND MONTH(s.created_at) = current_month
    ) current_data,
    (
        SELECT SUM(si.quantity * si.price) AS total_revenue
        FROM sales s
        JOIN sale_items si ON s.sale_id = si.sale_id
        WHERE YEAR(s.created_at) = prev_year
          AND MONTH(s.created_at) = prev_month
    ) previous_data;
END //


CREATE PROCEDURE search_products_advanced(
    IN p_query VARCHAR(255)
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.description,
        p.sku,
        p.unit_price,
        c.name AS category_name
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    WHERE p.name LIKE CONCAT('%', p_query, '%')
       OR p.description LIKE CONCAT('%', p_query, '%')
       OR p.sku LIKE CONCAT('%', p_query, '%')
       OR c.name LIKE CONCAT('%', p_query, '%');
END //


CREATE PROCEDURE get_top_products_by_revenue(
    IN limit_n INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        SUM(si.quantity) AS total_units_sold,
        SUM(si.quantity * si.price) AS total_revenue
    FROM sale_items si
    JOIN products p ON si.product_id = p.product_id
    JOIN sales s ON si.sale_id = s.sale_id
    WHERE s.created_at BETWEEN start_date AND end_date
    GROUP BY p.product_id, p.name
    ORDER BY total_revenue DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_least_sold_products(
    IN limit_n INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        IFNULL(SUM(si.quantity), 0) AS total_units_sold
    FROM products p
    LEFT JOIN sale_items si ON p.product_id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.sale_id
        AND s.created_at BETWEEN start_date AND end_date
    GROUP BY p.product_id, p.name
    ORDER BY total_units_sold ASC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_warehouse_inventory_value(
    IN p_warehouse_id INT
)
BEGIN
    SELECT
        w.warehouse_id,
        w.name AS warehouse_name,
        SUM(s.quantity * p.unit_price) AS inventory_value
    FROM stock s
    JOIN products p ON s.product_id = p.product_id
    JOIN warehouses w ON s.warehouse_id = w.warehouse_id
    WHERE w.warehouse_id = p_warehouse_id
    GROUP BY w.warehouse_id, w.name;
END //


CREATE PROCEDURE get_top_warehouses_by_stock()
BEGIN
    SELECT
        w.warehouse_id,
        w.name AS warehouse_name,
        SUM(s.quantity) AS total_units
    FROM warehouses w
    JOIN stock s ON w.warehouse_id = s.warehouse_id
    GROUP BY w.warehouse_id, w.name
    ORDER BY total_units DESC;
END //


CREATE PROCEDURE get_warehouse_low_stock_products(
    IN p_warehouse_id INT,
    IN threshold INT
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        s.quantity
    FROM stock s
    JOIN products p ON s.product_id = p.product_id
    WHERE s.warehouse_id = p_warehouse_id
      AND s.quantity < threshold
    ORDER BY s.quantity ASC;
END //


CREATE PROCEDURE get_supplier_spend(
    IN p_supplier_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        s.supplier_id,
        s.name AS supplier_name,
        SUM(pi.quantity * pi.price) AS total_spend
    FROM suppliers s
    JOIN purchases p ON s.supplier_id = p.supplier_id
    JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    WHERE s.supplier_id = p_supplier_id
      AND p.created_at BETWEEN start_date AND end_date
    GROUP BY s.supplier_id, s.name;
END //


CREATE PROCEDURE get_top_suppliers(
    IN limit_n INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        s.supplier_id,
        s.name AS supplier_name,
        SUM(pi.quantity * pi.price) AS total_spend
    FROM suppliers s
    JOIN purchases p ON s.supplier_id = p.supplier_id
    JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    WHERE p.created_at BETWEEN start_date AND end_date
    GROUP BY s.supplier_id, s.name
    ORDER BY total_spend DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_out_of_stock_products()
BEGIN
    SELECT
        p.product_id,
        p.name,
        IFNULL(SUM(s.quantity), 0) AS total_stock
    FROM products p
    LEFT JOIN stock s ON p.product_id = s.product_id
    GROUP BY p.product_id, p.name
    HAVING total_stock <= 0;
END //


CREATE PROCEDURE get_products_needing_restock(
    IN p_days_window INT,
    IN p_min_days_remaining FLOAT
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        SUM(st.quantity) AS current_stock,
        AVG(si.quantity) AS avg_daily_sales,
        SUM(st.quantity) / NULLIF(AVG(si.quantity), 0) AS estimated_days_remaining
    FROM products p
    JOIN stock st ON p.product_id = st.product_id
    LEFT JOIN sale_items si
        ON p.product_id = si.product_id
    LEFT JOIN sales s
        ON si.sale_id = s.sale_id
       AND s.created_at >= NOW() - INTERVAL p_days_window DAY
    GROUP BY p.product_id, p.name
    HAVING estimated_days_remaining < p_min_days_remaining
    ORDER BY estimated_days_remaining ASC;
END //


CREATE PROCEDURE get_products_without_recent_sales(
    IN p_days INT
)
BEGIN
    SELECT
        p.product_id,
        p.name
    FROM products p
    LEFT JOIN sale_items si ON p.product_id = si.product_id
    LEFT JOIN sales s ON si.sale_id = s.sale_id
    GROUP BY p.product_id, p.name
    HAVING MAX(s.created_at) IS NULL
       OR MAX(s.created_at) < NOW() - INTERVAL p_days DAY;
END //


CREATE PROCEDURE get_daily_revenue(
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        DATE(s.created_at) AS day,
        SUM(si.quantity * si.price) AS revenue
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    WHERE s.created_at BETWEEN start_date AND end_date
    GROUP BY DATE(s.created_at)
    ORDER BY day;
END //


CREATE PROCEDURE get_daily_product_sales(
    IN p_product_id INT,
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT
        DATE(s.created_at) AS day,
        SUM(si.quantity) AS units_sold
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    WHERE si.product_id = p_product_id
      AND s.created_at BETWEEN start_date AND end_date
    GROUP BY DATE(s.created_at)
    ORDER BY day;
END //


CREATE PROCEDURE get_monthly_revenue_by_category(
    IN p_year INT
)
BEGIN
    SELECT
        MONTH(s.created_at) AS month_number,
        c.category_id,
        c.name AS category_name,
        SUM(si.quantity * si.price) AS revenue
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    JOIN products p ON si.product_id = p.product_id
    JOIN categories c ON p.category_id = c.category_id
    WHERE YEAR(s.created_at) = p_year
    GROUP BY MONTH(s.created_at), c.category_id, c.name
    ORDER BY month_number, revenue DESC;
END //


CREATE PROCEDURE get_all_categories()
BEGIN
    SELECT
        c.category_id,
        c.name
    FROM categories c
    ORDER BY c.name;
END //


CREATE PROCEDURE get_all_products()
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        c.name AS category_name,
        p.unit_price,
        p.created_at
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    ORDER BY p.name;
END //


CREATE PROCEDURE get_all_warehouses()
BEGIN
    SELECT
        warehouse_id,
        name,
        location
    FROM warehouses
    ORDER BY name;
END //


CREATE PROCEDURE get_all_suppliers()
BEGIN
    SELECT
        supplier_id,
        name,
        contact_info
    FROM suppliers
    ORDER BY name;
END //


CREATE PROCEDURE get_all_users()
BEGIN
    SELECT
        user_id,
        name,
        email,
        permission_level
    FROM users
    ORDER BY name;
END //


CREATE PROCEDURE get_product_lookup()
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        c.name AS category_name,
        p.unit_price,
        IFNULL(SUM(s.quantity), 0) AS current_stock
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN stock s ON p.product_id = s.product_id
    GROUP BY
        p.product_id,
        p.name,
        p.sku,
        c.name,
        p.unit_price
    ORDER BY p.name;
END //


CREATE PROCEDURE get_product_lookup_by_category(
    IN p_category_id INT
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        p.unit_price,
        IFNULL(SUM(s.quantity), 0) AS current_stock
    FROM products p
    LEFT JOIN stock s ON p.product_id = s.product_id
    WHERE p.category_id = p_category_id
    GROUP BY
        p.product_id,
        p.name,
        p.sku,
        p.unit_price
    ORDER BY p.name;
END //


CREATE PROCEDURE get_product_lookup_by_name(
    IN p_name_query VARCHAR(255)
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        c.name AS category_name,
        p.unit_price,
        IFNULL(SUM(s.quantity), 0) AS current_stock
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN stock s ON p.product_id = s.product_id
    WHERE p.name LIKE CONCAT('%', p_name_query, '%')
    GROUP BY
        p.product_id,
        p.name,
        p.sku,
        c.name,
        p.unit_price
    ORDER BY p.name;
END //


CREATE PROCEDURE get_product_lookup_by_sku(
    IN p_sku_query VARCHAR(100)
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        c.name AS category_name,
        p.unit_price,
        IFNULL(SUM(s.quantity), 0) AS current_stock
    FROM products p
    LEFT JOIN categories c ON p.category_id = c.category_id
    LEFT JOIN stock s ON p.product_id = s.product_id
    WHERE p.sku LIKE CONCAT('%', p_sku_query, '%')
    GROUP BY
        p.product_id,
        p.name,
        p.sku,
        c.name,
        p.unit_price
    ORDER BY p.name;
END //


CREATE PROCEDURE get_category_lookup()
BEGIN
    SELECT
        c.category_id,
        c.name,
        COUNT(DISTINCT p.product_id) AS total_products
    FROM categories c
    LEFT JOIN products p ON c.category_id = p.category_id
    GROUP BY c.category_id, c.name
    ORDER BY c.name;
END //


CREATE PROCEDURE get_warehouse_lookup()
BEGIN
    SELECT
        w.warehouse_id,
        w.name,
        w.location,
        COUNT(DISTINCT s.product_id) AS unique_products,
        IFNULL(SUM(s.quantity), 0) AS total_units
    FROM warehouses w
    LEFT JOIN stock s ON w.warehouse_id = s.warehouse_id
    GROUP BY
        w.warehouse_id,
        w.name,
        w.location
    ORDER BY w.name;
END //


CREATE PROCEDURE get_warehouse_products(
    IN p_warehouse_id INT
)
BEGIN
    SELECT
        p.product_id,
        p.name,
        p.sku,
        s.quantity
    FROM stock s
    JOIN products p ON s.product_id = p.product_id
    WHERE s.warehouse_id = p_warehouse_id
    ORDER BY p.name;
END //


CREATE PROCEDURE get_supplier_lookup()
BEGIN
    SELECT
        s.supplier_id,
        s.name,
        COUNT(DISTINCT p.purchase_id) AS total_purchases,
        IFNULL(SUM(pi.quantity * pi.price), 0) AS lifetime_spend
    FROM suppliers s
    LEFT JOIN purchases p ON s.supplier_id = p.supplier_id
    LEFT JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    GROUP BY s.supplier_id, s.name
    ORDER BY s.name;
END //


CREATE PROCEDURE get_supplier_products(
    IN p_supplier_id INT
)
BEGIN
    SELECT
        pr.product_id,
        pr.name,
        pr.sku,
        SUM(pi.quantity) AS total_units_purchased,
        AVG(pi.price) AS avg_purchase_price
    FROM purchases pu
    JOIN purchase_items pi ON pu.purchase_id = pi.purchase_id
    JOIN products pr ON pi.product_id = pr.product_id
    WHERE pu.supplier_id = p_supplier_id
    GROUP BY
        pr.product_id,
        pr.name,
        pr.sku
    ORDER BY total_units_purchased DESC;
END //


CREATE PROCEDURE get_sales_lookup(
    IN limit_n INT
)
BEGIN
    SELECT
        s.sale_id,
        s.created_at,
        COUNT(si.sale_item_id) AS total_items,
        SUM(si.quantity * si.price) AS total_value
    FROM sales s
    LEFT JOIN sale_items si ON s.sale_id = si.sale_id
    GROUP BY s.sale_id, s.created_at
    ORDER BY s.created_at DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_sale_details(
    IN p_sale_id INT
)
BEGIN
    SELECT
        s.sale_id,
        s.created_at,
        p.product_id,
        p.name AS product_name,
        si.quantity,
        si.price,
        si.quantity * si.price AS subtotal
    FROM sales s
    JOIN sale_items si ON s.sale_id = si.sale_id
    JOIN products p ON si.product_id = p.product_id
    WHERE s.sale_id = p_sale_id
    ORDER BY p.name;
END //


CREATE PROCEDURE get_purchases_lookup(
    IN limit_n INT
)
BEGIN
    SELECT
        p.purchase_id,
        p.created_at,
        s.supplier_id,
        s.name AS supplier_name,
        COUNT(pi.purchase_item_id) AS total_items,
        SUM(pi.quantity * pi.price) AS total_cost
    FROM purchases p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    LEFT JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    GROUP BY
        p.purchase_id,
        p.created_at,
        s.supplier_id,
        s.name
    ORDER BY p.created_at DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_purchase_details(
    IN p_purchase_id INT
)
BEGIN
    SELECT
        p.purchase_id,
        p.created_at,
        s.supplier_id,
        s.name AS supplier_name,
        pr.product_id,
        pr.name AS product_name,
        pi.quantity,
        pi.price,
        pi.quantity * pi.price AS subtotal
    FROM purchases p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    JOIN purchase_items pi ON p.purchase_id = pi.purchase_id
    JOIN products pr ON pi.product_id = pr.product_id
    WHERE p.purchase_id = p_purchase_id
    ORDER BY pr.name;
END //


CREATE PROCEDURE get_recent_stock_movements(
    IN limit_n INT
)
BEGIN
    SELECT
        sm.movement_id,
        sm.created_at,
        p.product_id,
        p.name AS product_name,
        w.warehouse_id,
        w.name AS warehouse_name,
        sm.quantity,
        sm.movement_type,
        sm.reference_id
    FROM stock_movements sm
    JOIN products p ON sm.product_id = p.product_id
    JOIN warehouses w ON sm.warehouse_id = w.warehouse_id
    ORDER BY sm.created_at DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_product_movement_lookup(
    IN p_product_id INT
)
BEGIN
    SELECT
        sm.movement_id,
        sm.created_at,
        w.warehouse_id,
        w.name AS warehouse_name,
        sm.quantity,
        sm.movement_type,
        sm.reference_id
    FROM stock_movements sm
    JOIN warehouses w ON sm.warehouse_id = w.warehouse_id
    WHERE sm.product_id = p_product_id
    ORDER BY sm.created_at DESC;
END //


CREATE PROCEDURE create_category(
    IN p_name VARCHAR(255)
)
BEGIN
    INSERT INTO categories (name)
    VALUES (p_name);

    SELECT LAST_INSERT_ID() AS category_id;
END //

CREATE PROCEDURE update_category(
    IN p_category_id INT,
    IN p_name VARCHAR(255)
)
BEGIN
    UPDATE categories
    SET name = p_name
    WHERE category_id = p_category_id;
END //


CREATE PROCEDURE create_product(
    IN p_name VARCHAR(255),
    IN p_description TEXT,
    IN p_sku VARCHAR(100),
    IN p_category_id INT,
    IN p_unit_price DECIMAL(10,2)
)
BEGIN
    INSERT INTO products (
        name,
        description,
        sku,
        category_id,
        unit_price
    )
    VALUES (
        p_name,
        p_description,
        p_sku,
        p_category_id,
        p_unit_price
    );

    SELECT LAST_INSERT_ID() AS product_id;
END //


CREATE PROCEDURE update_product(
    IN p_product_id INT,
    IN p_name VARCHAR(255),
    IN p_description TEXT,
    IN p_sku VARCHAR(100),
    IN p_category_id INT,
    IN p_unit_price DECIMAL(10,2)
)
BEGIN
    UPDATE products
    SET
        name = p_name,
        description = p_description,
        sku = p_sku,
        category_id = p_category_id,
        unit_price = p_unit_price
    WHERE product_id = p_product_id;
END //


CREATE PROCEDURE create_warehouse(
    IN p_name VARCHAR(255),
    IN p_location VARCHAR(255)
)
BEGIN
    INSERT INTO warehouses (name, location)
    VALUES (p_name, p_location);

    SELECT LAST_INSERT_ID() AS warehouse_id;
END //


CREATE PROCEDURE update_warehouse(
    IN p_warehouse_id INT,
    IN p_name VARCHAR(255),
    IN p_location VARCHAR(255)
)
BEGIN
    UPDATE warehouses
    SET
        name = p_name,
        location = p_location
    WHERE warehouse_id = p_warehouse_id;
END //


CREATE PROCEDURE create_supplier(
    IN p_name VARCHAR(255),
    IN p_contact_info TEXT
)
BEGIN
    INSERT INTO suppliers (name, contact_info)
    VALUES (p_name, p_contact_info);

    SELECT LAST_INSERT_ID() AS supplier_id;
END //


CREATE PROCEDURE update_supplier(
    IN p_supplier_id INT,
    IN p_name VARCHAR(255),
    IN p_contact_info TEXT
)
BEGIN
    UPDATE suppliers
    SET
        name = p_name,
        contact_info = p_contact_info
    WHERE supplier_id = p_supplier_id;
END //


CREATE PROCEDURE create_user (
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    IN p_permission_level ENUM('end_user', 'admin')
)
BEGIN
    IF NOT EXISTS (
        SELECT u.email
        FROM users u
        WHERE u.email = p_email
    ) THEN
        INSERT INTO users (name, email, password, permission_level)
        VALUES (p_name, p_email, p_password, p_permission_level);
    ELSE
        SIGNAL SQLSTATE '45001'
        SET MESSAGE_TEXT = 'Email already in use';
    END IF;
END //


CREATE PROCEDURE update_user(
    IN p_user_id INT,
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_permission_level ENUM('end_user', 'admin')
)
BEGIN
    UPDATE users
    SET
        name = p_name,
        email = p_email,
        permission_level = p_permission_level
    WHERE user_id = p_user_id;
END //


CREATE PROCEDURE create_purchase(
    IN p_supplier_id INT
)
BEGIN
    INSERT INTO purchases (supplier_id)
    VALUES (p_supplier_id);

    SELECT purchase_id 
    FROM purchases
    WHERE purchase_id = LAST_INSERT_ID();
END //


CREATE PROCEDURE add_purchase_item(
    IN p_purchase_id INT,
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_quantity INT,
    IN p_price DECIMAL(10,2)
)
BEGIN
    DECLARE v_exists INT DEFAULT 0;

    START TRANSACTION;

    INSERT INTO purchase_items (
        purchase_id,
        product_id,
        quantity,
        price
    )
    VALUES (
        p_purchase_id,
        p_product_id,
        p_quantity,
        p_price
    );

    SELECT COUNT(*)
    INTO v_exists
    FROM stock
    WHERE product_id = p_product_id
      AND warehouse_id = p_warehouse_id;

    IF v_exists > 0 THEN
        UPDATE stock
        SET quantity = quantity + p_quantity
        WHERE product_id = p_product_id
          AND warehouse_id = p_warehouse_id;
    ELSE
        INSERT INTO stock (
            product_id,
            warehouse_id,
            quantity
        )
        VALUES (
            p_product_id,
            p_warehouse_id,
            p_quantity
        );
    END IF;

    INSERT INTO stock_movements (
        product_id,
        warehouse_id,
        quantity,
        movement_type,
        reference_id
    )
    VALUES (
        p_product_id,
        p_warehouse_id,
        p_quantity,
        'IN',
        p_purchase_id
    );

    COMMIT;
END //


CREATE PROCEDURE create_sale()
BEGIN
    INSERT INTO sales ()
    VALUES ();

    SELECT sale_id
    FROM sales
    WHERE sale_id = LAST_INSERT_ID();
END //


CREATE PROCEDURE add_sale_item(
    IN p_sale_id INT,
    IN p_product_id INT,
    IN p_warehouse_id INT,
    IN p_quantity INT,
    IN p_price DECIMAL(10,2)
)
BEGIN
    DECLARE v_current_stock INT DEFAULT 0;

    START TRANSACTION;

    SELECT quantity
    INTO v_current_stock
    FROM stock
    WHERE product_id = p_product_id
      AND warehouse_id = p_warehouse_id
    LIMIT 1;

    IF v_current_stock IS NULL OR v_current_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient stock for sale';
    END IF;

    INSERT INTO sale_items (
        sale_id,
        product_id,
        quantity,
        price
    )
    VALUES (
        p_sale_id,
        p_product_id,
        p_quantity,
        p_price
    );

    UPDATE stock
    SET quantity = quantity - p_quantity
    WHERE product_id = p_product_id
      AND warehouse_id = p_warehouse_id;

    INSERT INTO stock_movements (
        product_id,
        warehouse_id,
        quantity,
        movement_type,
        reference_id
    )
    VALUES (
        p_product_id,
        p_warehouse_id,
        p_quantity,
        'OUT',
        p_sale_id
    );

    COMMIT;
END //
