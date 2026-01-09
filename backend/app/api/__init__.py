"""
API endpoints for the wine inventory management system admin panel
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import crud, schemas


router = APIRouter(prefix="/api/v1", tags=["admin"])


# Wine endpoints
@router.get("/wines/", response_model=List[schemas.Wine])
def read_wines(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    vintage_year: Optional[int] = Query(None),
    producer: Optional[str] = Query(None),
    country: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve wines with optional filters
    """
    wines = crud.get_wines(
        db, 
        skip=skip, 
        limit=limit, 
        vintage_year=vintage_year,
        producer=producer,
        country=country
    )
    return wines


@router.get("/wines/{wine_id}", response_model=schemas.Wine)
def read_wine(wine_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific wine by ID
    """
    wine = crud.get_wine(db, wine_id=wine_id)
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine


@router.post("/wines/", response_model=schemas.Wine, status_code=status.HTTP_201_CREATED)
def create_wine(wine: schemas.WineCreate, db: Session = Depends(get_db)):
    """
    Create a new wine
    """
    return crud.create_wine(db=db, wine=wine)


@router.put("/wines/{wine_id}", response_model=schemas.Wine)
def update_wine(wine_id: int, wine_update: schemas.WineUpdate, db: Session = Depends(get_db)):
    """
    Update a wine
    """
    wine = crud.update_wine(db=db, wine_id=wine_id, wine_update=wine_update)
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine


@router.delete("/wines/{wine_id}", response_model=schemas.Wine)
def delete_wine(wine_id: int, db: Session = Depends(get_db)):
    """
    Delete a wine
    """
    wine = crud.delete_wine(db=db, wine_id=wine_id)
    if not wine:
        raise HTTPException(status_code=404, detail="Wine not found")
    return wine


# Inventory endpoints
@router.get("/inventories/", response_model=List[schemas.Inventory])
def read_inventories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    wine_id: Optional[int] = Query(None),
    location_type: Optional[schemas.LocationType] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve inventories with optional filters
    """
    inventories = crud.get_inventories(
        db, 
        skip=skip, 
        limit=limit, 
        wine_id=wine_id,
        location_type=location_type.value if location_type else None
    )
    return inventories


@router.get("/inventories/{inventory_id}", response_model=schemas.Inventory)
def read_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific inventory by ID
    """
    inventory = crud.get_inventory(db, inventory_id=inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.post("/inventories/", response_model=schemas.Inventory, status_code=status.HTTP_201_CREATED)
def create_inventory(inventory: schemas.InventoryCreate, db: Session = Depends(get_db)):
    """
    Create a new inventory entry or update existing one
    """
    return crud.create_inventory(db=db, inventory=inventory)


@router.put("/inventories/{inventory_id}", response_model=schemas.Inventory)
def update_inventory(
    inventory_id: int, 
    inventory_update: schemas.InventoryUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an inventory entry
    """
    inventory = crud.update_inventory(
        db=db, 
        inventory_id=inventory_id, 
        inventory_update=inventory_update
    )
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


@router.delete("/inventories/{inventory_id}", response_model=schemas.Inventory)
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    """
    Delete an inventory entry
    """
    inventory = crud.delete_inventory(db=db, inventory_id=inventory_id)
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory


# Sales endpoints
@router.get("/sales/", response_model=List[schemas.Sale])
def read_sales(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    wine_id: Optional[int] = Query(None),
    location_type: Optional[schemas.LocationType] = Query(None),
    sale_type: Optional[schemas.SaleType] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve sales with optional filters
    """
    sales = crud.get_sales(
        db, 
        skip=skip, 
        limit=limit, 
        wine_id=wine_id,
        location_type=location_type.value if location_type else None,
        sale_type=sale_type.value if sale_type else None
    )
    return sales


@router.get("/sales/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific sale by ID
    """
    sale = crud.get_sale(db, sale_id=sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.post("/sales/", response_model=schemas.Sale, status_code=status.HTTP_201_CREATED)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """
    Create a new sale and update inventory accordingly
    """
    try:
        return crud.create_sale(db=db, sale=sale)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/sales/{sale_id}", response_model=schemas.Sale)
def update_sale(sale_id: int, sale_update: schemas.SaleUpdate, db: Session = Depends(get_db)):
    """
    Update a sale
    """
    sale = crud.update_sale(db=db, sale_id=sale_id, sale_update=sale_update)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


@router.delete("/sales/{sale_id}", response_model=schemas.Sale)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    """
    Delete a sale and restore inventory
    """
    sale = crud.delete_sale(db=db, sale_id=sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale


# Orders endpoints
@router.get("/orders/", response_model=List[schemas.Order])
def read_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    customer_email: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve orders with optional filters
    """
    orders = crud.get_orders(
        db, 
        skip=skip, 
        limit=limit, 
        status=status,
        customer_email=customer_email
    )
    return orders


@router.get("/orders/{order_id}", response_model=schemas.Order)
def read_order(order_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific order by ID
    """
    order = crud.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("/orders/", response_model=schemas.Order, status_code=status.HTTP_201_CREATED)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order and update inventory
    """
    try:
        return crud.create_order(db=db, order=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/orders/{order_id}", response_model=schemas.Order)
def update_order(order_id: int, order_update: schemas.OrderUpdate, db: Session = Depends(get_db)):
    """
    Update an order
    """
    order = crud.update_order(db=db, order_id=order_id, order_update=order_update)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/orders/{order_id}", response_model=schemas.Order)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    """
    Delete an order and restore inventory
    """
    order = crud.delete_order(db=db, order_id=order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# Adjustments endpoints
@router.get("/adjustments/", response_model=List[schemas.Adjustment])
def read_adjustments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    wine_id: Optional[int] = Query(None),
    location_type: Optional[schemas.LocationType] = Query(None),
    adjustment_type: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve adjustments with optional filters
    """
    adjustments = crud.get_adjustments(
        db, 
        skip=skip, 
        limit=limit, 
        wine_id=wine_id,
        location_type=location_type.value if location_type else None,
        adjustment_type=adjustment_type
    )
    return adjustments


@router.get("/adjustments/{adjustment_id}", response_model=schemas.Adjustment)
def read_adjustment(adjustment_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific adjustment by ID
    """
    adjustment = crud.get_adjustment(db, adjustment_id=adjustment_id)
    if not adjustment:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adjustment


@router.post("/adjustments/", response_model=schemas.Adjustment, status_code=status.HTTP_201_CREATED)
def create_adjustment(adjustment: schemas.AdjustmentCreate, db: Session = Depends(get_db)):
    """
    Create a new adjustment and update inventory
    """
    return crud.create_adjustment(db=db, adjustment=adjustment)


@router.delete("/adjustments/{adjustment_id}", response_model=schemas.Adjustment)
def delete_adjustment(adjustment_id: int, db: Session = Depends(get_db)):
    """
    Delete an adjustment and revert the changes
    """
    adjustment = crud.delete_adjustment(db=db, adjustment_id=adjustment_id)
    if not adjustment:
        raise HTTPException(status_code=404, detail="Adjustment not found")
    return adjustment


# Reports and Analytics endpoints
@router.get("/reports/inventory-details", response_model=List[schemas.InventoryWithWineDetails])
def get_inventory_report(db: Session = Depends(get_db)):
    """
    Get detailed inventory report with wine information and calculated values
    """
    return crud.get_inventory_with_details(db)


@router.get("/reports/sales-summary", response_model=List[schemas.SaleSummary])
def get_sales_summary_report(db: Session = Depends(get_db)):
    """
    Get aggregated sales summary report
    """
    return crud.get_sales_summary(db)