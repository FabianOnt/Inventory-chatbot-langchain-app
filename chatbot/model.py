from collections import defaultdict
import gc
import torch
import os

from datetime import datetime
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, AIMessageChunk

from chatbot.tools import (
    get_product_stock,
    get_low_stock,
    get_inventory_by_warehouse,
    search_products,
    get_stock_movements,
    get_net_stock_change,
    get_stock_trend,
    get_total_sales,
    get_top_products,
    get_slow_moving_products,
    get_inventory_turnover,
    get_days_of_inventory,
    estimate_demand,
    transfer_stock,
    create_user,
    get_category_sales,
    get_category_stock,
    get_top_categories,
    get_categories_without_sales,
    get_monthly_sales_summary,
    get_monthly_purchase_summary,
    get_monthly_category_sales,
    get_month_over_month_growth,
    search_products_advanced,
    get_top_products_by_revenue,
    get_least_sold_products,
    get_warehouse_inventory_value,
    get_top_warehouses_by_stock,
    get_warehouse_low_stock_products,
    get_supplier_spend,
    get_top_suppliers,
    get_out_of_stock_products,
    get_products_needing_restock,
    get_products_without_recent_sales,
    get_daily_revenue,
    get_daily_product_sales,
    get_monthly_revenue_by_category,
    get_all_categories,
    get_all_products,
    get_all_warehouses,
    get_all_suppliers,
    get_all_users,
    create_category,
    update_category,
    create_product,
    update_product,
    create_warehouse,
    update_warehouse,
    create_supplier,
    update_supplier,
    update_user,
)


TOOL_GROUPS = {
    "inventory": [
        get_product_stock,
        get_products_needing_restock,
        get_low_stock,
        get_inventory_by_warehouse,
        get_stock_movements,
        get_net_stock_change,
        get_stock_trend,
        get_out_of_stock_products,
    ],

    "sales": [
        get_total_sales,
        get_top_products,
        get_daily_revenue,
        get_top_products_by_revenue,
        get_daily_product_sales,
        get_monthly_sales_summary,
        get_slow_moving_products,
        get_least_sold_products,
        get_month_over_month_growth,
    ],

    "warehouse": [
        get_all_warehouses,
        get_top_warehouses_by_stock,
        get_warehouse_inventory_value,
        get_inventory_by_warehouse,
        get_warehouse_low_stock_products,
        transfer_stock,
        create_warehouse,
        update_warehouse,
    ],

    "suppliers": [
        get_all_suppliers,
        get_supplier_spend,
        get_top_suppliers,
        create_supplier,
        update_supplier,
    ],

    "products": [
        search_products,
        search_products_advanced,
        get_all_products,
        create_product,
        update_product,
    ],

    "categories": [
        get_all_categories,
        get_category_sales,
        get_category_stock,
        get_top_categories,
        get_categories_without_sales,
        get_monthly_category_sales,
        get_monthly_revenue_by_category,
        create_category,
        update_category
    ],

    "forecasting": [
        estimate_demand,
        get_inventory_turnover,
        get_days_of_inventory,
        get_products_without_recent_sales,
    ],

    "admin": [
        create_user,
        update_user,
        get_all_users,
    ],
}


ROLE_ALLOWED_GROUPS = {
    "admin": {
        "inventory",
        "sales",
        "warehouse",
        "suppliers",
        "products",
        "categories",
        "forecasting",
        "admin",
    },

    "end_user": {
        "inventory",
        "sales",
        "warehouse",
        "suppliers",
        "products",
        "categories",
        "forecasting",
    }
}


# tool router
KEYWORD_TO_GROUP = {
    "inventory": [
        "stock", "inventory", "restock", "movement", "movements",
        "out of stock", "low stock", "warehouse stock", "net stock"
    ],

    "sales": [
        "sales", "revenue", "sold", "best selling", "top selling",
        "growth", "profit", "income", "monthly sales", "daily sales"
    ],

    "warehouse": [
        "warehouse", "warehouses", "transfer", "move stock",
        "warehouse inventory"
    ],

    "suppliers": [
        "supplier", "suppliers", "vendor", "vendors", "supplier spend"
    ],

    "products": [
        "product", "products", "sku", "search", "item"
    ],

    "categories": [
        "category", "categories"
    ],

    "forecasting": [
        "forecast", "demand", "estimate", "turnover",
        "days of inventory", "slow moving"
    ],

    "admin": [
        "create user", "update user", "new user", "manage user"
    ]
}


def detect_groups_from_query(query: str) -> list[str]:
    query_lower = query.lower()
    selected_groups = []

    for group_name, keywords in KEYWORD_TO_GROUP.items():
        if any(keyword in query_lower for keyword in keywords):
            selected_groups.append(group_name)

    # Always include products because many queries start by identifying products
    if "products" not in selected_groups:
        selected_groups.append("products")

    # Default fallback if nothing was detected
    if len(selected_groups) == 1 and selected_groups[0] == "products":
        selected_groups.extend(["inventory"])

    # Remove duplicates while preserving order
    selected_groups = list(dict.fromkeys(selected_groups))

    return selected_groups


def get_tools_for_query(query: str, user_role: str = "admin", max_tools: int = 10):
    detected_groups = detect_groups_from_query(query)

    allowed_groups = ROLE_ALLOWED_GROUPS.get(user_role, set())

    final_groups = [
        group for group in detected_groups
        if group in allowed_groups
    ]

    selected_tools = []
    added_tool_names = set()

    for group in final_groups:
        for tool in TOOL_GROUPS[group]:
            tool_name = tool.name

            if tool_name not in added_tool_names:
                selected_tools.append(tool)
                added_tool_names.add(tool_name)

    return selected_tools[:max_tools], final_groups


def build_system_prompt(tool_groups: list[str], user_role: str) -> str:
    return f"""
You are an assistant for querying and executing operations in the inventory of a company.

The current user role is: {user_role}

You currently have access only to the following tool groups:
{', '.join(tool_groups)}

Guidelines:
- Use tools whenever possible instead of guessing.
- If a product must be identified first, use a product search tool.
- If the available tools are insufficient, clearly explain what information is missing.
- Do not invent product IDs, warehouse IDs, supplier IDs, or category IDs.
- If the user asks for an operation not available in the current tool set, explain that it is unavailable.
- Keep responses concise and operational.
- Today is {datetime.now()} and if no temporal data included, assume this month [Today - start of the month].
- Each limit, window_size, treshold or min_days, etc. parameter in tools must be greater than 0.
- start_date parameter is inclusive and end_date parameters is exclusive.
""".strip()


agent_cache = {}


def get_or_create_agent(model, tools_for_query, tool_groups, user_role):
    cache_key = (
        tuple(sorted(tool.name for tool in tools_for_query)),
        user_role,
    )

    if cache_key not in agent_cache:
        system_prompt = build_system_prompt(tool_groups, user_role)

        agent_cache[cache_key] = create_agent(
            model,
            tools=tools_for_query,
            system_prompt=system_prompt,
        )

    return agent_cache[cache_key]


def start_chatbot():
    model = ChatOllama(
        model="qwen3.5:latest",
        reasoning=False,
        temperature=0.3,
        keep_alive=-1
    )

    return model


def start_chat(model, user_role: str = "admin"):
    os.system("cls")
    print("""
======================================================================
Welcome to the Inventory Operations Assistant
======================================================================
I can help you query and manage products, stock, warehouses,
suppliers, sales, purchases, and other inventory operations.

Examples:
- Which are the best selling products this month?
- Show products with low stock
- Search product 'Laptop Dell Inspiron'
- List warehouses in Puebla
- Show recent sales from the last 7 days
- Create a new supplier

Type /exit or /quit to close the chat.
======================================================================
""")

    messages = []

    while True:
        user_input = input("User: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["/exit", "/quit"]:
            print("Chat closed.")
            break

        tools_for_query, tool_groups = get_tools_for_query(
            query=user_input,
            user_role=user_role,
            max_tools=20,
        )

        agent = get_or_create_agent(
            model=model,
            tools_for_query=tools_for_query,
            tool_groups=tool_groups,
            user_role=user_role,
        )

        messages.append(HumanMessage(content=user_input))

        try:
            print("Agent: ", end="", flush=True)

            full_response = ""

            for chunk in agent.stream(
                {"messages": messages},
                stream_mode="values"
            ):
                if "messages" not in chunk:
                    continue

                last_message = chunk["messages"][-1]

                if isinstance(last_message, AIMessageChunk):
                    if last_message.content:
                        print(last_message.content, end="", flush=True)
                        full_response += last_message.content

                elif isinstance(last_message, AIMessage):
                    if last_message.content and last_message.content != full_response:
                        new_text = last_message.content[len(full_response):]
                        print(new_text, end="", flush=True)
                        full_response = last_message.content

            print()

            if full_response.strip():
                messages.append(AIMessage(content=full_response))

        except Exception as e:
            print(f"\nAgent Error: {e}")

        print("\n")


def shutdown_chatbot(model):
    del model

    gc.collect()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()