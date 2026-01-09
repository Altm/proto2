"""
CRUD operations for the wine inventory management system
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from decimal import Decimal
from typing import List, Optional
from ..models import Wine, Inventory, Sale, Order, OrderItem, Adjustment
from ..schemas import (
    WineCreate, WineUpdate, 
    InventoryCreate, InventoryUpdate,
    SaleCreate, SaleUpdate,
    OrderCreate, OrderUpdate,
    OrderItemCreate,
    AdjustmentCreate
)


# Wine CRUD operations
def get_wine(db: Session, wine_id: int):
    return db.query(Wine).filter(Wine.id == wine_id).first()


def get_wine_by_uuid(db: Session, uuid: str):
    return db.query(Wine).filter(Wine.uuid == uuid).first()


def get_wines(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    vintage_year: Optional[int] = None,
    producer: Optional[str] = None,
    country: Optional[str] = None
):
    query = db.query(Wine)
    
    if vintage_year:
        query = query.filter(Wine.vintage_year == vintage_year)
    if producer:
        query = query.filter(Wine.producer.ilike(f"%{producer}%"))
    if country:
        query = query.filter(Wine.country.ilike(f"%{country}%"))
    
    return query.offset(skip).limit(limit).all()


def create_wine(db: Session, wine: WineCreate):
    db_wine = Wine(**wine.model_dump())
    db.add(db_wine)
    db.commit()
    db.refresh(db_wine)
    return db_wine


def update_wine(db: Session, wine_id: int, wine_update: WineUpdate):
    db_wine = db.query(Wine).filter(Wine.id == wine_id).first()
    if db_wine:
        update_data = wine_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_wine, field, value)
        db.commit()
        db.refresh(db_wine)
    return db_wine


def delete_wine(db: Session, wine_id: int):
    db_wine = db.query(Wine).filter(Wine.id == wine_id).first()
    if db_wine:
        db.delete(db_wine)
        db.commit()
    return db_wine


# Inventory CRUD operations
def get_inventory(db: Session, inventory_id: int):
    return db.query(Inventory).filter(Inventory.id == inventory_id).first()


def get_inventory_by_location_and_wine(db: Session, wine_id: int, location_type: str):
    return db.query(Inventory).filter(
        Inventory.wine_id == wine_id,
        Inventory.location_type == location_type
    ).first()


def get_inventories(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    wine_id: Optional[int] = None,
    location_type: Optional[str] = None
):
    query = db.query(Inventory).join(Wine)
    
    if wine_id:
        query = query.filter(Inventory.wine_id == wine_id)
    if location_type:
        query = query.filter(Inventory.location_type == location_type)
    
    return query.offset(skip).limit(limit).all()


def create_inventory(db: Session, inventory: InventoryCreate):
    # Check if inventory for this wine and location already exists
    existing_inventory = get_inventory_by_location_and_wine(
        db, inventory.wine_id, inventory.location_type
    )
    
    if existing_inventory:
        # Update existing inventory instead of creating a new one
        existing_inventory.bottles_count += inventory.bottles_count
        db.commit()
        db.refresh(existing_inventory)
        return existing_inventory
    else:
        db_inventory = Inventory(**inventory.model_dump())
        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)
        return db_inventory


def update_inventory(db: Session, inventory_id: int, inventory_update: InventoryUpdate):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory:
        update_data = inventory_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_inventory, field, value)
        db.commit()
        db.refresh(db_inventory)
    return db_inventory


def delete_inventory(db: Session, inventory_id: int):
    db_inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if db_inventory:
        db.delete(db_inventory)
        db.commit()
    return db_inventory


# Sale CRUD operations
def get_sale(db: Session, sale_id: int):
    return db.query(Sale).filter(Sale.id == sale_id).first()


def get_sales(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    wine_id: Optional[int] = None,
    location_type: Optional[str] = None,
    sale_type: Optional[str] = None
):
    query = db.query(Sale).join(Wine)
    
    if wine_id:
        query = query.filter(Sale.wine_id == wine_id)
    if location_type:
        query = query.filter(Sale.location_type == location_type)
    if sale_type:
        query = query.filter(Sale.sale_type == sale_type)
    
    return query.order_by(Sale.sale_date.desc()).offset(skip).limit(limit).all()


def create_sale(db: Session, sale: SaleCreate):
    # Calculate total amount
    total_amount = sale.quantity * sale.unit_price
    
    # Create the sale record
    db_sale = Sale(
        wine_id=sale.wine_id,
        sale_type=sale.sale_type,
        quantity=sale.quantity,
        unit_price=sale.unit_price,
        total_amount=total_amount,
        location_type=sale.location_type,
        notes=sale.notes
    )
    db.add(db_sale)
    
    # Update inventory based on the sale
    inventory = get_inventory_by_location_and_wine(db, sale.wine_id, sale.location_type)
    if inventory:
        # Calculate how much to reduce from inventory
        if sale.sale_type == "bottle":
            reduction = sale.quantity
        else:  # glass
            # Find the wine to get glasses per bottle
            wine = get_wine(db, sale.wine_id)
            if wine:
                reduction = sale.quantity / wine.glasses_per_bottle
            else:
                reduction = sale.quantity / 5  # default
        
        # Check if we have enough inventory
        if inventory.bottles_count < reduction:
            raise ValueError(f"Not enough inventory. Available: {inventory.bottles_count}, Required: {reduction}")
        
        # Update inventory
        inventory.bottles_count -= reduction
    else:
        # Create inventory entry if it doesn't exist (should not happen in normal flow)
        raise ValueError(f"No inventory found for wine {sale.wine_id} at location {sale.location_type}")
    
    db.commit()
    db.refresh(db_sale)
    return db_sale


def update_sale(db: Session, sale_id: int, sale_update: SaleUpdate):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale:
        update_data = sale_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_sale, field, value)
        db.commit()
        db.refresh(db_sale)
    return db_sale


def delete_sale(db: Session, sale_id: int):
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale:
        # Need to restore inventory when deleting a sale
        inventory = get_inventory_by_location_and_wine(db, db_sale.wine_id, db_sale.location_type)
        if inventory:
            if db_sale.sale_type == "bottle":
                restoration = db_sale.quantity
            else:  # glass
                wine = get_wine(db, db_sale.wine_id)
                if wine:
                    restoration = db_sale.quantity / wine.glasses_per_bottle
                else:
                    restoration = db_sale.quantity / 5  # default
            
            inventory.bottles_count += restoration
        
        db.delete(db_sale)
        db.commit()
    return db_sale


# Order CRUD operations
def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_by_uuid(db: Session, uuid: str):
    return db.query(Order).filter(Order.uuid == uuid).first()


def get_orders(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    status: Optional[str] = None,
    customer_email: Optional[str] = None
):
    query = db.query(Order)
    
    if status:
        query = query.filter(Order.status == status)
    if customer_email:
        query = query.filter(Order.customer_email.ilike(f"%{customer_email}%"))
    
    return query.order_by(Order.order_date.desc()).offset(skip).limit(limit).all()


def create_order(db: Session, order: OrderCreate):
    # Calculate total amount from order items
    total_amount = sum(item.quantity * item.unit_price for item in order.order_items)
    
    # Create the order
    db_order = Order(
        customer_name=order.customer_name,
        customer_email=order.customer_email,
        shipping_address=order.shipping_address,
        postal_code=order.postal_code,
        country=order.country,
        total_amount=total_amount,
        shipping_cost=0,  # Will be calculated later based on shipping rules
        status="pending",
        notes=order.notes
    )
    db.add(db_order)
    db.flush()  # Get the order ID without committing
    
    # Create order items and update inventory
    order_total = 0
    for item_data in order.order_items:
        # Calculate item total
        item_total = item_data.quantity * item_data.unit_price
        
        # Create order item
        order_item = OrderItem(
            order_id=db_order.id,
            wine_id=item_data.wine_id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total_price=item_total
        )
        db.add(order_item)
        
        # Update inventory (for online sales, always bottles)
        inventory = get_inventory_by_location_and_wine(db, item_data.wine_id, "warehouse")
        if inventory:
            if inventory.bottles_count < item_data.quantity:
                raise ValueError(f"Not enough inventory for wine {item_data.wine_id}. Available: {inventory.bottles_count}, Required: {item_data.quantity}")
            
            inventory.bottles_count -= item_data.quantity
        else:
            raise ValueError(f"No warehouse inventory found for wine {item_data.wine_id}")
        
        order_total += item_total
    
    db_order.total_amount = order_total
    db.commit()
    db.refresh(db_order)
    return db_order


def update_order(db: Session, order_id: int, order_update: OrderUpdate):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        update_data = order_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_order, field, value)
        db.commit()
        db.refresh(db_order)
    return db_order


def delete_order(db: Session, order_id: int):
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if db_order:
        # Restore inventory when deleting an order
        for item in db_order.order_items:
            inventory = get_inventory_by_location_and_wine(db, item.wine_id, "warehouse")
            if inventory:
                inventory.bottles_count += item.quantity
        
        db.delete(db_order)
        db.commit()
    return db_order


# Adjustment CRUD operations
def get_adjustment(db: Session, adjustment_id: int):
    return db.query(Adjustment).filter(Adjustment.id == adjustment_id).first()


def get_adjustments(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    wine_id: Optional[int] = None,
    location_type: Optional[str] = None,
    adjustment_type: Optional[str] = None
):
    query = db.query(Adjustment).join(Wine)
    
    if wine_id:
        query = query.filter(Adjustment.wine_id == wine_id)
    if location_type:
        query = query.filter(Adjustment.location_type == location_type)
    if adjustment_type:
        query = query.filter(Adjustment.adjustment_type == adjustment_type)
    
    return query.order_by(Adjustment.adjustment_date.desc()).offset(skip).limit(limit).all()


def create_adjustment(db: Session, adjustment: AdjustmentCreate):
    db_adjustment = Adjustment(**adjustment.model_dump())
    db.add(db_adjustment)
    
    # Update inventory based on adjustment
    inventory = get_inventory_by_location_and_wine(db, adjustment.wine_id, adjustment.location_type)
    if inventory:
        inventory.bottles_count += adjustment.quantity
    else:
        # Create new inventory entry if it doesn't exist
        inventory = Inventory(
            wine_id=adjustment.wine_id,
            location_type=adjustment.location_type,
            bottles_count=adjustment.quantity
        )
        db.add(inventory)
    
    db.commit()
    db.refresh(db_adjustment)
    return db_adjustment


def delete_adjustment(db: Session, adjustment_id: int):
    db_adjustment = db.query(Adjustment).filter(Adjustment.id == adjustment_id).first()
    if db_adjustment:
        # Revert the adjustment by changing the sign
        inventory = get_inventory_by_location_and_wine(db, db_adjustment.wine_id, db_adjustment.location_type)
        if inventory:
            inventory.bottles_count -= db_adjustment.quantity  # Subtract because we're reverting
        
        db.delete(db_adjustment)
        db.commit()
    return db_adjustment


# Utility functions for reports and analytics
def get_inventory_with_details(db: Session):
    """Get inventory with wine details and calculated values"""
    result = db.query(
        Inventory.id,
        Inventory.wine_id,
        Inventory.location_type,
        Inventory.bottles_count,
        (Inventory.bottles_count * Wine.glasses_per_bottle).label('glasses_count'),
        Wine.name.label('wine_name'),
        Wine.producer.label('wine_producer'),
        Wine.country.label('wine_country'),
        Wine.region.label('wine_region'),
        Wine.vintage_year.label('wine_vintage_year'),
        Wine.glasses_per_bottle.label('wine_glasses_per_bottle')
    ).join(Wine, Inventory.wine_id == Wine.id).all()
    
    return result


def get_sales_summary(db: Session):
    """Get aggregated sales data grouped by wine and location"""
    result = db.query(
        Sale.wine_id,
        Wine.name.label('wine_name'),
        Wine.vintage_year,
        Sale.location_type,
        func.sum(case((Sale.sale_type == 'bottle', Sale.quantity)).else_(Sale.quantity / Wine.glasses_per_bottle)).label('total_sold_bottles'),
        func.sum(case((Sale.sale_type == 'bottle', Sale.quantity * Wine.glasses_per_bottle)).else_(Sale.quantity)).label('total_sold_glasses'),
        func.sum(Sale.total_amount).label('total_revenue')
    ).join(Wine, Sale.wine_id == Wine.id).group_by(
        Sale.wine_id, Wine.name, Wine.vintage_year, Sale.location_type
    ).all()
    
    return result