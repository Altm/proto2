from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime, date
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal, Product, Inventory, Sale, Promotion, InventoryAdjustment

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Wine Shop API", version="1.0.0")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models
class ProductBase(BaseModel):
    name: str
    category: str
    producer: str
    country: str
    region: str
    vintage: Optional[int] = None
    price: Optional[float] = None
    product_type: str = 'bottle'  # 'bottle' or 'glass'
    description: Optional[str] = None
    active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InventoryBase(BaseModel):
    product_id: int
    location: str
    current_stock: int = 0
    reserved_stock: int = 0

class InventoryCreate(InventoryBase):
    pass

class InventoryResponse(InventoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class SaleBase(BaseModel):
    product_id: int
    customer_name: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float
    status: str = 'completed'

class SaleCreate(SaleBase):
    pass

class SaleResponse(SaleBase):
    id: int
    sale_date: Optional[datetime] = None

    class Config:
        from_attributes = True

class PromotionBase(BaseModel):
    name: str
    type: str  # 'five_plus_one', 'free_shipping', 'percentage_discount', 'fixed_discount'
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    active: bool = True
    conditions: Optional[dict] = None

class PromotionCreate(PromotionBase):
    pass

class PromotionResponse(PromotionBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class InventoryAdjustmentBase(BaseModel):
    product_id: int
    old_stock: int
    new_stock: int
    adjustment_reason: str  # 'count_correction', 'breakage', 'tasting', 'other'
    notes: Optional[str] = None
    adjusted_by: str

class InventoryAdjustmentCreate(InventoryAdjustmentBase):
    pass

class InventoryAdjustmentResponse(InventoryAdjustmentBase):
    id: int
    adjusted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# Routes

@app.get("/")
def read_root():
    return {"message": "Wine Shop API"}

@app.get("/products", response_model=List[ProductResponse])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of products"""
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@app.post("/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product entry"""
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    """Update a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product_update.model_dump().items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a specific product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@app.get("/inventory", response_model=List[InventoryResponse])
def get_inventory(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get current inventory"""
    inventory = db.query(Inventory).offset(skip).limit(limit).all()
    return inventory

@app.post("/inventory", response_model=InventoryResponse)
def create_inventory(inventory: InventoryCreate, db: Session = Depends(get_db)):
    """Create a new inventory record"""
    db_inventory = Inventory(**inventory.model_dump())
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

@app.get("/inventory/product/{product_id}", response_model=List[InventoryResponse])
def get_inventory_by_product(product_id: int, db: Session = Depends(get_db)):
    """Get inventory for a specific product"""
    inventory = db.query(Inventory).filter(Inventory.product_id == product_id).all()
    if not inventory:
        raise HTTPException(status_code=404, detail="No inventory found for this product")
    return inventory

@app.put("/inventory/{inventory_id}", response_model=InventoryResponse)
def update_inventory(inventory_id: int, inventory_update: InventoryCreate, db: Session = Depends(get_db)):
    """Update a specific inventory record"""
    inventory = db.query(Inventory).filter(Inventory.id == inventory_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    for key, value in inventory_update.model_dump().items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    return inventory

@app.post("/sales", response_model=SaleResponse)
def create_sale(sale: SaleCreate, db: Session = Depends(get_db)):
    """Record a new sale"""
    # Check if there's enough inventory
    inventory = db.query(Inventory).filter(Inventory.product_id == sale.product_id).first()
    if not inventory or inventory.current_stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough inventory for this sale")
    
    # Create sale record
    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    
    # Update inventory
    inventory.current_stock -= sale.quantity
    db.commit()
    
    return db_sale

@app.get("/sales", response_model=List[SaleResponse])
def get_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of sales"""
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales

@app.post("/promotions", response_model=PromotionResponse)
def create_promotion(promotion: PromotionCreate, db: Session = Depends(get_db)):
    """Create a new promotion"""
    db_promotion = Promotion(**promotion.model_dump())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion

@app.get("/promotions", response_model=List[PromotionResponse])
def get_promotions(skip: int = 0, limit: int = 100, active_only: bool = True, db: Session = Depends(get_db)):
    """Get all promotions"""
    query = db.query(Promotion)
    if active_only:
        query = query.filter(Promotion.active == True)
    promotions = query.offset(skip).limit(limit).all()
    return promotions

@app.get("/promotions/type/{promo_type}", response_model=List[PromotionResponse])
def get_promotions_by_type(promo_type: str, active_only: bool = True, db: Session = Depends(get_db)):
    """Get promotions by type"""
    query = db.query(Promotion).filter(Promotion.type == promo_type)
    if active_only:
        query = query.filter(Promotion.active == True)
    promotions = query.all()
    return promotions

@app.post("/inventory-adjustments", response_model=InventoryAdjustmentResponse)
def create_inventory_adjustment(adjustment: InventoryAdjustmentCreate, db: Session = Depends(get_db)):
    """Create a new inventory adjustment"""
    # Get current inventory
    inventory = db.query(Inventory).filter(Inventory.product_id == adjustment.product_id).first()
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found for this product")
    
    # Validate the adjustment
    if inventory.current_stock != adjustment.old_stock:
        raise HTTPException(status_code=400, detail=f"Current stock ({inventory.current_stock}) does not match old stock ({adjustment.old_stock})")
    
    # Create adjustment record
    db_adjustment = InventoryAdjustment(**adjustment.model_dump())
    db.add(db_adjustment)
    
    # Update inventory
    inventory.current_stock = adjustment.new_stock
    db.commit()
    
    db.refresh(db_adjustment)
    return db_adjustment

@app.get("/inventory-adjustments", response_model=List[InventoryAdjustmentResponse])
def get_inventory_adjustments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get list of inventory adjustments"""
    adjustments = db.query(InventoryAdjustment).offset(skip).limit(limit).all()
    return adjustments

@app.get("/reports/inventory")
def get_inventory_report(db: Session = Depends(get_db)):
    """Get comprehensive inventory report"""
    inventory_items = db.query(Inventory).all()
    report = []
    
    for item in inventory_items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            report.append({
                "product_id": product.id,
                "product_name": product.name,
                "category": product.category,
                "producer": product.producer,
                "country": product.country,
                "region": product.region,
                "vintage": product.vintage,
                "product_type": product.product_type,
                "location": item.location,
                "current_stock": item.current_stock,
                "reserved_stock": item.reserved_stock,
                "total_available": item.current_stock - item.reserved_stock
            })
    
    return report

@app.get("/reports/sales")
def get_sales_report(start_date: Optional[str] = None, end_date: Optional[str] = None, db: Session = Depends(get_db)):
    """Get sales report with optional date filtering"""
    query = db.query(Sale)
    
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        query = query.filter(Sale.sale_date >= start_dt)
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        query = query.filter(Sale.sale_date <= end_dt)
    
    sales = query.all()
    
    total_sales = len(sales)
    total_revenue = sum(sale.total_price for sale in sales)
    
    # Group by product
    sales_by_product = {}
    for sale in sales:
        product = db.query(Product).filter(Product.id == sale.product_id).first()
        if product:
            key = f"{product.name} ({product.vintage})"
            if key not in sales_by_product:
                sales_by_product[key] = {
                    "product_name": product.name,
                    "vintage": product.vintage,
                    "product_type": product.product_type,
                    "total_quantity_sold": 0,
                    "total_revenue": 0.0
                }
            sales_by_product[key]["total_quantity_sold"] += sale.quantity
            sales_by_product[key]["total_revenue"] += sale.total_price
    
    return {
        "summary": {
            "total_sales": total_sales,
            "total_revenue": total_revenue,
        },
        "sales_by_product": list(sales_by_product.values()),
        "detailed_sales": [
            {
                "id": sale.id,
                "product_id": sale.product_id,
                "customer_name": sale.customer_name,
                "quantity": sale.quantity,
                "unit_price": sale.unit_price,
                "total_price": sale.total_price,
                "sale_date": sale.sale_date,
                "status": sale.status
            } for sale in sales
        ]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)