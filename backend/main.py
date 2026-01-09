from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(title="Wine Shop API", version="1.0.0")

# Pydantic models
class WineBase(BaseModel):
    name: str
    producer: str
    country: str
    region: str
    year: int
    price_bottle: float
    price_glass: float
    quantity_bottles: int
    quantity_glasses: int
    description: Optional[str] = None

class WineCreate(WineBase):
    pass

class Wine(WineBase):
    id: int

    class Config:
        from_attributes = True

class SaleItem(BaseModel):
    wine_id: int
    quantity: int
    unit_type: str  # 'bottle' or 'glass'
    unit_price: float

class SaleCreate(BaseModel):
    items: List[SaleItem]
    total_amount: float

class InventoryReport(BaseModel):
    wine_id: int
    wine_name: str
    year: int
    bottles_available: int
    glasses_available: int

class PromotionBase(BaseModel):
    name: str
    description: str
    active: bool

class PromotionCreate(PromotionBase):
    pass

class Promotion(PromotionBase):
    id: int

    class Config:
        from_attributes = True

# Mock data storage
wines_db = []
sales_db = []
promotions_db = []

# Routes

@app.get("/")
def read_root():
    return {"message": "Wine Shop API"}

@app.get("/wines", response_model=List[Wine])
def get_wines(skip: int = 0, limit: int = 100):
    """Get list of wines"""
    return wines_db[skip: skip + limit]

@app.post("/wines", response_model=Wine)
def create_wine(wine: WineCreate):
    """Create a new wine entry"""
    wine_obj = Wine(
        id=len(wines_db) + 1,
        **wine.model_dump()
    )
    wines_db.append(wine_obj)
    return wine_obj

@app.get("/wines/{wine_id}", response_model=Wine)
def get_wine(wine_id: int):
    """Get a specific wine by ID"""
    for wine in wines_db:
        if wine.id == wine_id:
            return wine
    raise HTTPException(status_code=404, detail="Wine not found")

@app.put("/wines/{wine_id}", response_model=Wine)
def update_wine(wine_id: int, wine_update: WineCreate):
    """Update a specific wine"""
    for i, wine in enumerate(wines_db):
        if wine.id == wine_id:
            updated_wine = Wine(
                id=wine_id,
                **wine_update.model_dump()
            )
            wines_db[i] = updated_wine
            return updated_wine
    raise HTTPException(status_code=404, detail="Wine not found")

@app.delete("/wines/{wine_id}")
def delete_wine(wine_id: int):
    """Delete a specific wine"""
    for i, wine in enumerate(wines_db):
        if wine.id == wine_id:
            wines_db.pop(i)
            return {"message": "Wine deleted successfully"}
    raise HTTPException(status_code=404, detail="Wine not found")

@app.post("/sales")
def create_sale(sale: SaleCreate):
    """Record a new sale"""
    sale_id = len(sales_db) + 1
    sale_dict = sale.model_dump()
    sale_dict['id'] = sale_id
    sales_db.append(sale_dict)
    
    # Update inventory based on sale
    for item in sale.items:
        for wine in wines_db:
            if wine.id == item.wine_id:
                if item.unit_type == 'bottle':
                    wine.quantity_bottles -= item.quantity
                elif item.unit_type == 'glass':
                    wine.quantity_glasses -= item.quantity
    
    return {"message": "Sale recorded successfully", "sale_id": sale_id}

@app.get("/inventory", response_model=List[InventoryReport])
def get_inventory():
    """Get current inventory report"""
    report = []
    for wine in wines_db:
        report_item = InventoryReport(
            wine_id=wine.id,
            wine_name=wine.name,
            year=wine.year,
            bottles_available=wine.quantity_bottles,
            glasses_available=wine.quantity_glasses
        )
        report.append(report_item)
    return report

@app.post("/promotions", response_model=Promotion)
def create_promotion(promotion: PromotionCreate):
    """Create a new promotion"""
    promo_obj = Promotion(
        id=len(promotions_db) + 1,
        **promotion.model_dump()
    )
    promotions_db.append(promo_obj)
    return promo_obj

@app.get("/promotions", response_model=List[Promotion])
def get_promotions():
    """Get all promotions"""
    return promotions_db

@app.get("/reports/sales")
def get_sales_report(start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Get sales report with optional date filtering"""
    return {
        "total_sales": len(sales_db),
        "total_revenue": sum(sale.get('total_amount', 0) for sale in sales_db),
        "sales_data": sales_db
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)