
import csv
from pathlib import Path
from datetime import date, timedelta
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("pharmacy-stock")

DATA = Path(__file__).parent / "data" / "pharmacy_stock.csv"
BACKUP = Path(__file__).parent / "data" / "pharmacy_stock_backup.csv"

def load_stock():
    with open(DATA, newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


@mcp.tool()
def check_stock(item: str, strength: str = "") -> list[dict]:
    """Check available stock for a medicine by name and optional strength."""
    return [
        row for row in load_stock()
        if item.lower() in row["item"].lower()
        and strength.lower() in row["strength"].lower()
    ]


@mcp.tool()
def search_items(query: str) -> list[dict]:
    """Search pharmacy inventory by medicine name, strength or form."""
    return [
        row for row in load_stock()
        if query.lower() in (
            row["item"] + " " + row["strength"] + " " + row["form"]
        ).lower()
    ]


@mcp.tool()
def list_expiring(days: int) -> list[dict]:
    """List medicines expiring within the specified number of days."""
    today = date.today()
    deadline = today + timedelta(days=days)

    return [
        row for row in load_stock()
        if today <= date.fromisoformat(row["expiry_date"]) <= deadline
    ]

@mcp.tool()
def record_sale(item: str, strength: str, quantity: int) -> dict:
    """Record a medicine sale and safely reduce its available stock."""

    # Safety check 1: Quantity must be positive
    if quantity <= 0:
        return {"success": False, "message": "Quantity must be greater than zero."}

    rows = load_stock()

    # Find the exact medicine and strength
    match = None
    for row in rows:
        if (
            row["item"].lower() == item.lower()
            and row["strength"].lower() == strength.lower()
        ):
            match = row
            break

    # Safety check 2: Medicine must exist
    if match is None:
        return {"success": False, "message": "Medicine or strength not found."}

    current_quantity = int(match["quantity"])

    # Safety check 3: Enough stock must be available
    if quantity > current_quantity:
        return {
            "success": False,
            "message": f"Insufficient stock. Only {current_quantity} available."
        }

    # Update the stock only after all checks pass
    match["quantity"] = str(current_quantity - quantity)

    fieldnames = list(rows[0].keys())

    with open(DATA, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    return {
        "success": True,
        "message": "Sale recorded successfully.",
        "item": item,
        "strength": strength,
        "quantity_sold": quantity,
        "remaining_stock": int(match["quantity"])
    }
if __name__ == "__main__":
    mcp.run()
