"""
GestorInventario — aplicación base (SUT) para el Reto AI-First · Track QA.

App full-stack mínima y autocontenida:
  - Backend: FastAPI
  - Base de datos: SQLite (archivo local, se crea y siembra solo)
  - Web service: API REST bajo /api
  - Integración: servicio de alertas de stock mínimo (/api/stock/alerts),
    con simulación de caída vía la variable de entorno ALERTS_FAIL=1
  - Frontend: página estática servida en /

Ejecutar:
    pip install -r requirements.txt
    uvicorn app:app --reload --port 8000
Luego abrir http://localhost:8000
"""
import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "inventario.db")

SEED_SUPPLIERS = [
    ("Distribuidora Central", "central@dist.co", "+57 310 1234567"),
    ("Importaciones Norte", "norte@import.co", "+57 320 9876543"),
    ("Suministros Rápidos", "rapidos@sum.co", "+57 300 5551234"),
]

# (name, sku, cost_cents, price_cents, stock, min_stock, supplier_id)
SEED_PRODUCTS = [
    ("Resma Papel Carta", "PAP-001", 8000, 12000, 50, 10, 1),
    ("Cartucho Tóner Negro", "TON-002", 45000, 68000, 12, 5, 2),
    ("Silla Ergonómica", "SIL-003", 250000, 380000, 8, 3, 3),
    ('Monitor 24"', "MON-004", 550000, 799000, 5, 2, 2),
    ("Teclado Inalámbrico", "TEC-005", 80000, 125000, 20, 5, 1),
    ("Mouse Óptico", "MOU-006", 35000, 52000, 35, 8, 1),
]


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with closing(get_conn()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS suppliers (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   email TEXT NOT NULL,
                   phone TEXT NOT NULL,
                   active INTEGER NOT NULL DEFAULT 1)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS products (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL,
                   sku TEXT NOT NULL UNIQUE,
                   cost_cents INTEGER NOT NULL,
                   price_cents INTEGER NOT NULL,
                   stock INTEGER NOT NULL DEFAULT 0,
                   min_stock INTEGER NOT NULL DEFAULT 0,
                   supplier_id INTEGER NOT NULL,
                   active INTEGER NOT NULL DEFAULT 1)"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS stock_movements (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   product_id INTEGER NOT NULL,
                   type TEXT NOT NULL,
                   qty REAL NOT NULL,
                   notes TEXT,
                   created_at TEXT NOT NULL)"""
        )
        if conn.execute("SELECT COUNT(*) AS c FROM suppliers").fetchone()["c"] == 0:
            conn.executemany(
                "INSERT INTO suppliers (name, email, phone) VALUES (?, ?, ?)",
                SEED_SUPPLIERS,
            )
        if conn.execute("SELECT COUNT(*) AS c FROM products").fetchone()["c"] == 0:
            conn.executemany(
                "INSERT INTO products (name, sku, cost_cents, price_cents, stock, min_stock, supplier_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                SEED_PRODUCTS,
            )


def alert_service(product_id: int) -> dict:
    """Servicio de alertas de stock mínimo. Lanza RuntimeError si se simula caída."""
    if os.environ.get("ALERTS_FAIL") == "1":
        raise RuntimeError("alert service unavailable")
    with closing(get_conn()) as conn:
        row = conn.execute(
            "SELECT name, stock, min_stock FROM products WHERE id = ?", (product_id,)
        ).fetchone()
    if row and row["stock"] <= row["min_stock"]:
        return {"alert": True, "product_id": product_id, "stock": row["stock"], "min_stock": row["min_stock"]}
    return {"alert": False, "product_id": product_id}


class ProductIn(BaseModel):
    name: str
    sku: str
    cost_cents: int
    price_cents: int
    stock: int = 0
    min_stock: int = 0
    supplier_id: int


class StockMovementIn(BaseModel):
    product_id: int
    type: str          # "IN" or "OUT"
    qty: float         # BUG: should be int — accepts decimals like 2.5
    notes: str = ""


app = FastAPI(title="GestorInventario", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup():
    init_db()


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/suppliers")
def list_suppliers():
    with closing(get_conn()) as conn:
        rows = conn.execute(
            "SELECT * FROM suppliers WHERE active = 1 ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


@app.get("/api/products")
def list_products():
    with closing(get_conn()) as conn:
        rows = conn.execute(
            "SELECT * FROM products WHERE active = 1 ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    with closing(get_conn()) as conn:
        row = conn.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,)
        ).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return dict(row)


@app.post("/api/products", status_code=201)
def create_product(product: ProductIn):
    with closing(get_conn()) as conn, conn:
        existing = conn.execute(
            "SELECT id FROM products WHERE sku = ?", (product.sku,)
        ).fetchone()
        if existing:
            raise HTTPException(status_code=409, detail="SKU ya existe")
        supplier = conn.execute(
            "SELECT id FROM suppliers WHERE id = ? AND active = 1", (product.supplier_id,)
        ).fetchone()
        if supplier is None:
            raise HTTPException(status_code=400, detail="Proveedor no encontrado")
        cur = conn.execute(
            """INSERT INTO products (name, sku, cost_cents, price_cents, stock, min_stock, supplier_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (product.name, product.sku, product.cost_cents, product.price_cents,
             product.stock, product.min_stock, product.supplier_id),
        )
    return get_product(cur.lastrowid)


@app.post("/api/stock/movement", status_code=201)
def register_movement(movement: StockMovementIn):
    if movement.type not in ("IN", "OUT"):
        raise HTTPException(status_code=400, detail="type debe ser IN o OUT")

    with closing(get_conn()) as conn, conn:
        product = conn.execute(
            "SELECT * FROM products WHERE id = ?", (movement.product_id,)
        ).fetchone()
        if product is None:
            raise HTTPException(status_code=404, detail="Producto no encontrado")

        # BUG: OUT movements do not validate qty <= current stock — stock can go negative
        delta = movement.qty if movement.type == "IN" else -movement.qty
        conn.execute(
            "UPDATE products SET stock = stock + ? WHERE id = ?",
            (delta, movement.product_id),
        )
        cur = conn.execute(
            """INSERT INTO stock_movements (product_id, type, qty, notes, created_at)
               VALUES (?, ?, ?, ?, ?)""",
            (movement.product_id, movement.type, movement.qty, movement.notes,
             datetime.now(timezone.utc).isoformat()),
        )
        movement_id = cur.lastrowid

    if movement.type == "OUT":
        try:
            alert_service(movement.product_id)
        except RuntimeError:
            raise HTTPException(status_code=503, detail="Servicio de alertas no disponible")

    with closing(get_conn()) as conn:
        row = conn.execute(
            "SELECT * FROM stock_movements WHERE id = ?", (movement_id,)
        ).fetchone()
    return dict(row)


@app.get("/api/stock/alerts")
def stock_alerts():
    try:
        if os.environ.get("ALERTS_FAIL") == "1":
            raise RuntimeError("alert service unavailable")
        with closing(get_conn()) as conn:
            rows = conn.execute(
                "SELECT * FROM products WHERE active = 1 AND stock <= min_stock ORDER BY stock ASC"
            ).fetchall()
            return [dict(r) for r in rows]
    except RuntimeError:
        raise HTTPException(status_code=503, detail="Servicio de alertas no disponible")


@app.get("/api/movements")
def list_movements():
    with closing(get_conn()) as conn:
        rows = conn.execute(
            "SELECT * FROM stock_movements ORDER BY id DESC"
        ).fetchall()
        return [dict(r) for r in rows]


# El frontend estático se monta al final para no tapar las rutas /api
app.mount("/", StaticFiles(directory="static", html=True), name="static")
