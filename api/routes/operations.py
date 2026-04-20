import uuid

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field, EmailStr
from typing import Literal

from api.routes.sessions import validate_request
from api.db.interface import get_connection, run_proc
from api.routes.sessions import redis_client

router = APIRouter(prefix="/operations", tags=["operations"])


class TransferStockRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    from_warehouse_id: int = Field(..., gt=0)
    to_warehouse_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class CreateUserRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=255)
    permission_level: Literal["end_user", "admin"]


class CreateCategoryRequest(BaseModel):
    name: str


class UpdateCategoryRequest(BaseModel):
    category_id: int = Field(..., gt=0)
    name: str


class CreateProductRequest(BaseModel):
    name: str
    description: str
    sku: str
    category_id: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class UpdateProductRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    name: str
    description: str
    sku: str
    category_id: int = Field(..., gt=0)
    unit_price: float = Field(..., gt=0)


class CreateWarehouseRequest(BaseModel):
    name: str
    location: str


class UpdateWarehouseRequest(BaseModel):
    warehouse_id: int = Field(..., gt=0)
    name: str
    location: str


class CreateSupplierRequest(BaseModel):
    name: str
    contact_info: str


class UpdateSupplierRequest(BaseModel):
    supplier_id: int = Field(..., gt=0)
    name: str
    contact_info: str


class UpdateUserRequest(BaseModel):
    user_id: int = Field(..., gt=0)
    name: str
    email: str
    permission_level: str


class CreatePurchaseRequest(BaseModel):
    supplier_id: int


class CreateSaleRequest(BaseModel):
    pass


class AddPurchaseItemRequest(BaseModel):
    purchase_session_key: str
    product_id: int
    warehouse_id: int
    quantity: int
    price: float


class AddSaleItemRequest(BaseModel):
    sale_session_key: str
    product_id: int
    warehouse_id: int
    quantity: int
    price: float


class ClosePurchaseRequest(BaseModel):
    purchase_session_key: str


class CloseSaleRequest(BaseModel):
    sale_session_key: str


@router.post("/transfer-stock")
def transfer_stock(request: Request, payload: TransferStockRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="transfer_stock",
            args=(
                payload.product_id,
                payload.from_warehouse_id,
                payload.to_warehouse_id,
                payload.quantity
            )
        )

        return {
            "message": "Stock transferred successfully",
            "product_id": payload.product_id,
            "from_warehouse_id": payload.from_warehouse_id,
            "to_warehouse_id": payload.to_warehouse_id,
            "quantity": payload.quantity
        }

    finally:
        conn.close()


@router.post("/create-user")
def create_user(request: Request, payload: CreateUserRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="create_user",
            args=(
                payload.name,
                payload.email,
                payload.password,
                payload.permission_level
            )
        )

        return {
            "message": "User created successfully",
            "email": payload.email,
            "permission_level": payload.permission_level
        }

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        conn.close()


@router.post("/create-category")
def create_category(request: Request, payload: CreateCategoryRequest):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="create_category",
            args=(payload.name,)
        )

        category_id = result[0][0]["category_id"] if result else None

        return {
            "message": "Category created successfully",
            "category_id": category_id,
            "name": payload.name
        }

    finally:
        conn.close()


@router.put("/update-category")
def update_category(request: Request, payload: UpdateCategoryRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="update_category",
            args=(
                payload.category_id,
                payload.name
            )
        )

        return {
            "message": "Category updated successfully",
            "category_id": payload.category_id
        }

    finally:
        conn.close()


@router.post("/create-product")
def create_product(request: Request, payload: CreateProductRequest):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="create_product",
            args=(
                payload.name,
                payload.description,
                payload.sku,
                payload.category_id,
                payload.unit_price
            )
        )

        product_id = result[0][0]["product_id"] if result else None

        return {
            "message": "Product created successfully",
            "product_id": product_id,
            "sku": payload.sku
        }

    finally:
        conn.close()


@router.put("/update-product")
def update_product(request: Request, payload: UpdateProductRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="update_product",
            args=(
                payload.product_id,
                payload.name,
                payload.description,
                payload.sku,
                payload.category_id,
                payload.unit_price
            )
        )

        return {
            "message": "Product updated successfully",
            "product_id": payload.product_id
        }

    finally:
        conn.close()


@router.post("/create-warehouse")
def create_warehouse(request: Request, payload: CreateWarehouseRequest):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="create_warehouse",
            args=(
                payload.name,
                payload.location
            )
        )

        warehouse_id = result[0][0]["warehouse_id"] if result else None

        return {
            "message": "Warehouse created successfully",
            "warehouse_id": warehouse_id,
            "name": payload.name
        }

    finally:
        conn.close()


@router.put("/update-warehouse")
def update_warehouse(request: Request, payload: UpdateWarehouseRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="update_warehouse",
            args=(
                payload.warehouse_id,
                payload.name,
                payload.location
            )
        )

        return {
            "message": "Warehouse updated successfully",
            "warehouse_id": payload.warehouse_id
        }

    finally:
        conn.close()


@router.post("/create-supplier")
def create_supplier(request: Request, payload: CreateSupplierRequest):
    validate_request(request)
    conn = get_connection()
    try:
        result = run_proc(
            conn=conn,
            proc="create_supplier",
            args=(
                payload.name,
                payload.contact_info
            )
        )

        supplier_id = result[0][0]["supplier_id"] if result else None

        return {
            "message": "Supplier created successfully",
            "supplier_id": supplier_id,
            "name": payload.name
        }

    finally:
        conn.close()


@router.put("/update-supplier")
def update_supplier(request: Request, payload: UpdateSupplierRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="update_supplier",
            args=(
                payload.supplier_id,
                payload.name,
                payload.contact_info
            )
        )

        return {
            "message": "Supplier updated successfully",
            "supplier_id": payload.supplier_id
        }

    finally:
        conn.close()


@router.put("/update-user")
def update_user(request: Request, payload: UpdateUserRequest):
    validate_request(request)
    conn = get_connection()
    try:
        run_proc(
            conn=conn,
            proc="update_user",
            args=(
                payload.user_id,
                payload.name,
                payload.email,
                payload.permission_level
            )
        )

        return {
            "message": "User updated successfully",
            "user_id": payload.user_id,
            "email": payload.email
        }

    finally:
        conn.close()


@router.post("/create-purchase")
def create_purchase(request: Request, payload: CreatePurchaseRequest):
    validate_request(request)
    conn = get_connection()

    try:
        result = run_proc(
            conn=conn,
            proc="create_purchase",
            args=(payload.supplier_id,)
        )

        purchase_id = result[0][0]["purchase_id"]

        purchase_session_key = str(uuid.uuid4())

        redis_client.setex(
            f"purchase_session:{purchase_session_key}",
            1800,
            purchase_id
        )

        return {
            "message": "Purchase created successfully",
            "purchase_session_key": purchase_session_key,
            "expires_in_seconds": 1800
        }

    finally:
        conn.close()


@router.post("/add-purchase-item")
def add_purchase_item(request: Request, payload: AddPurchaseItemRequest):
    validate_request(request)
    conn = get_connection()

    try:
        purchase_id = redis_client.get(
            f"purchase_session:{payload.purchase_session_key}"
        )

        if not purchase_id:
            return {
                "error": "Purchase session expired or invalid"
            }

        run_proc(
            conn=conn,
            proc="add_purchase_item",
            args=(
                int(purchase_id),
                payload.product_id,
                payload.warehouse_id,
                payload.quantity,
                payload.price
            )
        )

        redis_client.expire(
            f"purchase_session:{payload.purchase_session_key}",
            1800
        )

        return {
            "message": "Purchase item added successfully"
        }

    finally:
        conn.close()


@router.post("/create-sale")
def create_sale(request: Request):
    validate_request(request)
    conn = get_connection()

    try:
        result = run_proc(
            conn=conn,
            proc="create_sale"
        )

        sale_id = result[0][0]["sale_id"]

        sale_session_key = str(uuid.uuid4())

        redis_client.setex(
            f"sale_session:{sale_session_key}",
            900,
            sale_id
        )

        return {
            "message": "Sale created successfully",
            "sale_session_key": sale_session_key,
            "expires_in_seconds": 900
        }

    finally:
        conn.close()


@router.post("/add-sale-item")
def add_sale_item(request: Request, payload: AddSaleItemRequest):
    validate_request(request)
    conn = get_connection()

    try:
        sale_id = redis_client.get(
            f"sale_session:{payload.sale_session_key}"
        )

        if not sale_id:
            return {
                "error": "Sale session expired or invalid"
            }

        run_proc(
            conn=conn,
            proc="add_sale_item",
            args=(
                int(sale_id),
                payload.product_id,
                payload.warehouse_id,
                payload.quantity,
                payload.price
            )
        )

        redis_client.expire(
            f"sale_session:{payload.sale_session_key}",
            900
        )

        return {
            "message": "Sale item added successfully"
        }

    finally:
        conn.close()


@router.post("/close-purchase")
def close_purchase(request: Request, payload: ClosePurchaseRequest):
    validate_request(request)

    redis_key = f"purchase_session:{payload.purchase_session_key}"
    purchase_id = redis_client.get(redis_key)

    if not purchase_id:
        return {
            "error": "Purchase session expired or invalid"
        }

    redis_client.delete(redis_key)

    return {
        "message": "Purchase session closed successfully",
        "purchase_id": int(purchase_id)
    }


@router.post("/close-sale")
def close_sale(request: Request, payload: CloseSaleRequest):
    validate_request(request)

    redis_key = f"sale_session:{payload.sale_session_key}"
    sale_id = redis_client.get(redis_key)

    if not sale_id:
        return {
            "error": "Sale session expired or invalid"
        }

    redis_client.delete(redis_key)

    return {
        "message": "Sale session closed successfully",
        "sale_id": int(sale_id)
    }

