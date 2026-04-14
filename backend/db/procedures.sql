-- BASIC QUERIES

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


-- MOVEMENT INSIGHTS

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


-- SALES INSIGHTS

CREATE PROCEDURE get_total_sales(
    IN start_date DATETIME,
    IN end_date DATETIME
)
BEGIN
    SELECT 
        SUM(quantity * price) AS total_revenue
    FROM sale_items
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
    JOIN products p ON si.product_id = p.product_id
    WHERE si.created_at BETWEEN start_date AND end_date
    GROUP BY p.product_id
    ORDER BY total_sold DESC
    LIMIT limit_n;
END //


CREATE PROCEDURE get_slow_moving_products(
    IN days INT
)
BEGIN
    SELECT p.product_id, p.name, IFNULL(SUM(si.quantity), 0) AS total_sold
    FROM products p
    LEFT JOIN sale_items si 
        ON p.product_id = si.product_id
        AND si.created_at >= NOW() - INTERVAL days DAY
    GROUP BY p.product_id
    HAVING total_sold = 0;
END //


-- INVENTORY ANALYSIS

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
    WHERE product_id = p_product_id
      AND created_at >= NOW() - INTERVAL 30 DAY;

    SELECT SUM(quantity) INTO current_stock
    FROM stock
    WHERE product_id = p_product_id;

    SELECT current_stock / NULLIF(daily_sales, 0) AS days_remaining;
END //


-- OPERATIONS

CREATE PROCEDURE estimate_demand(
    IN p_product_id INT,
    IN window_days INT
)
BEGIN
    SELECT AVG(quantity) AS avg_daily_demand
    FROM sale_items
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


-- SESSION LOGIN
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


CREATE PROCEDURE create_user (
    IN p_name VARCHAR(255),
    IN p_email VARCHAR(255),
    IN p_password VARCHAR(255),
    IN permission_level ENUM('end_user', 'admin')
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