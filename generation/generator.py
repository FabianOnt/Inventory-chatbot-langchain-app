import random
import string
import csv
import math

from core.client import APIClient
from collections import defaultdict
from core.client import APIClient

from config.config import (
    APP_ADMIN_USER,
    APP_ADMIN_PASSWORD,
    HOST,
    PORT
)

from generation.config import (
    CATEGORIES,
    WAREHOUSES,
    SUPPLIER_PREFIXES,
    SUPPLIER_SUFIXES,
    PRODUCT_NAMES_BY_CATEGORY,
    SAMPLE_USERS,
    SUPPLIER_CATEGORY_PREFERENCES
)


BASE_URL = f"http://{HOST}:{PORT}"
USERNAME = APP_ADMIN_USER
PASSWORD = APP_ADMIN_PASSWORD


def random_sku(prefix: str) -> str:
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix[:3].upper()}-{suffix}"


def populate_database():
    global BASE_URL, USERNAME, PASSWORD

    client = APIClient(base_url=BASE_URL)

    client.login(
        username=USERNAME,
        password=PASSWORD
    )

    category_id_map = {}
    warehouse_ids = []
    supplier_ids = []
    supplier_names = []
    product_records = []

    for category_name in CATEGORIES:
        client.create_category(name=category_name)

    all_categories = client.get_all_categories().get("categories", [])

    for category in all_categories:
        category_id_map[category["name"]] = category["category_id"]


    for warehouse_name, location in WAREHOUSES:
        response = client.create_warehouse(
            name=warehouse_name,
            location=location
        )
        warehouse_ids.append(response["warehouse_id"])

    used_supplier_names = set()

    while len(supplier_names) < 20:
        supplier_name = (
            f"{random.choice(SUPPLIER_PREFIXES)} "
            f"{random.choice(SUPPLIER_SUFIXES)}"
        )

        if supplier_name in used_supplier_names:
            continue

        used_supplier_names.add(supplier_name)

        email_slug = supplier_name.lower().replace(' ', '.')
        contact_info = (
            f"contact@{email_slug}.com | +52 55 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
        )

        response = client.create_supplier(
            name=supplier_name,
            contact_info=contact_info
        )

        supplier_ids.append(response["supplier_id"])
        supplier_names.append(supplier_name)


    product_counter = 0
    target_products = 120

    while product_counter < target_products:
        category_name = random.choice(CATEGORIES)
        product_name = random.choice(PRODUCT_NAMES_BY_CATEGORY[category_name])

        variation = random.choice([
            "Pro", "Max", "Lite", "Plus", "Mini",
            "Advanced", "Premium", "XL", "2026 Edition", ""
        ])

        full_name = f"{product_name} {variation}".strip()

        description = (
            f"High-quality {full_name.lower()} for {category_name.lower()} applications. "
            f"Designed for durability, performance, and everyday use."
        )

        sku = random_sku(product_name)

        if category_name in ["Electronics", "Computers", "Gaming"]:
            unit_price = round(random.uniform(50, 2500), 2)
        elif category_name in ["Furniture", "Fitness", "Home Appliances"]:
            unit_price = round(random.uniform(80, 1800), 2)
        elif category_name in ["Books", "Office Supplies", "Toys"]:
            unit_price = round(random.uniform(5, 150), 2)
        else:
            unit_price = round(random.uniform(10, 500), 2)

        response = client.create_product(
            name=full_name,
            description=description,
            sku=sku,
            category_id=category_id_map[category_name],
            unit_price=unit_price
        )

        product_records.append({
            "product_id": response["product_id"],
            "name": full_name,
            "category": category_name,
            "unit_price": unit_price
        })

        product_counter += 1


    supplier_price_matrix = []
    product_supplier_options = defaultdict(list)

    csv_header = ["product_id", "product_name"] + supplier_names
    csv_rows = []

    for product in product_records:
        row = [product["product_id"], product["name"]]

        for supplier_index, supplier_id in enumerate(supplier_ids):
            preferred_categories = SUPPLIER_CATEGORY_PREFERENCES.get(
                supplier_index % len(SUPPLIER_CATEGORY_PREFERENCES),
                []
            )

            category_match = product["category"] in preferred_categories

            if category_match:
                offered_probability = 0.85
            else:
                offered_probability = 0.15

            if random.random() < offered_probability:
                supplier_price = round(
                    product["unit_price"] * random.uniform(0.65, 0.95),
                    2
                )

                supplier_price_matrix.append({
                    "supplier_id": supplier_id,
                    "product_id": product["product_id"],
                    "price": supplier_price
                })

                product_supplier_options[product["product_id"]].append({
                    "supplier_id": supplier_id,
                    "price": supplier_price
                })

                row.append(supplier_price)
            else:
                row.append(math.inf)

        csv_rows.append(row)

    with open("generation/supplier_price_matrix.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(csv_header)
        writer.writerows(csv_rows)

    stock_tracker = defaultdict(int)

    for supplier_id in supplier_ids:
        num_purchases = random.randint(2, 5)

        supplier_products = [
            item for item in supplier_price_matrix
            if item["supplier_id"] == supplier_id
        ]

        if not supplier_products:
            continue

        for _ in range(num_purchases):
            purchase_response = client.create_purchase(
                supplier_id=supplier_id
            )

            purchase_session_key = purchase_response["purchase_session_key"]

            selected_products = random.sample(
                supplier_products,
                k=min(random.randint(3, 10), len(supplier_products))
            )

            for product_data in selected_products:
                quantity = random.randint(5, 100)
                warehouse_id = random.choice(warehouse_ids)

                client.add_purchase_item(
                    purchase_session_key=purchase_session_key,
                    product_id=product_data["product_id"],
                    warehouse_id=warehouse_id,
                    quantity=quantity,
                    price=product_data["price"]
                )

                stock_tracker[
                    (product_data["product_id"], warehouse_id)
                ] += quantity

            client.close_purchase(
                purchase_session_key=purchase_session_key
            )

    cheapest_supplier_price_by_product = {}

    for item in supplier_price_matrix:
        product_id = item["product_id"]
        price = item["price"]

        if (
            product_id not in cheapest_supplier_price_by_product
            or price < cheapest_supplier_price_by_product[product_id]
        ):
            cheapest_supplier_price_by_product[product_id] = price

    for product in product_records:
        product_id = product["product_id"]

        if product_id in cheapest_supplier_price_by_product:
            new_store_price = round(
                cheapest_supplier_price_by_product[product_id] * 1.10,
                2
            )

            client.update_product(
                product_id=product_id,
                name=product["name"],
                description=(
                    f"High-quality {product['name'].lower()} for {product['category'].lower()} applications. "
                    f"Designed for durability, performance, and everyday use."
                ),
                sku=f"AUTO-{product_id}",
                category_id=category_id_map[product["category"]],
                unit_price=new_store_price
            )

            product["unit_price"] = new_store_price


    for _ in range(60):
        available_stock_entries = [
            {
                "product_id": product_id,
                "warehouse_id": warehouse_id,
                "available_quantity": quantity
            }
            for (product_id, warehouse_id), quantity in stock_tracker.items()
            if quantity > 0
        ]

        if not available_stock_entries:
            break

        sale_response = client.create_sale()
        sale_session_key = sale_response["sale_session_key"]

        num_items = min(
            random.randint(1, 5),
            len(available_stock_entries)
        )

        selected_entries = random.sample(
            available_stock_entries,
            k=num_items
        )

        for stock_entry in selected_entries:
            product_id = stock_entry["product_id"]
            warehouse_id = stock_entry["warehouse_id"]
            available_quantity = stock_entry["available_quantity"]

            product = next(
                p for p in product_records
                if p["product_id"] == product_id
            )

            quantity_to_sell = random.randint(
                1,
                min(available_quantity, 3)
            )

            try:
                client.add_sale_item(
                    sale_session_key=sale_session_key,
                    product_id=product_id,
                    warehouse_id=warehouse_id,
                    quantity=quantity_to_sell,
                    price=product["unit_price"]
                )

                stock_tracker[(product_id, warehouse_id)] -= quantity_to_sell

            except Exception:
                continue

        client.close_sale(
            sale_session_key=sale_session_key
        )


    for name, email, password, permission_level in SAMPLE_USERS:
        client.create_user(
            name=name,
            email=email,
            password=password,
            permission_level=permission_level
        )

    client.logout()