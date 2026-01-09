"""
Pydantic schemas for the wine inventory management system
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from decimal import Decimal


class WineType(str, Enum):
    RED = "red"
    WHITE = "white"
    ROSE = "rose"
    SPARKLING = "sparkling"
    DESSERT = "dessert"
    FORTIFIED = "fortified"


class LocationType(str, Enum):
    WAREHOUSE = "warehouse"
    BAR_RESTAURANT = "bar_restaurant"


class SaleType(str, Enum):
    BOTTLE = "bottle"
    GLASS = "glass"


class WineBase(BaseModel):
    name: str = Field(..., description="Name of the wine")
    producer: str = Field(..., description="Producer/winery of the wine")
    country: str = Field(..., description="Country of origin")
    region: str = Field(..., description="Region of origin")
    volume_ml: int = Field(..., gt=0, description="Volume of bottle in milliliters")
    vintage_year: int = Field(..., ge=1800, le=2100, description="Vintage year of the wine")
    glasses_per_bottle: int = Field(default=5, gt=0, description="Number of glasses per bottle")
    type: Optional[WineType] = None
    rating: Optional[float] = Field(None, ge=0, le=10, description="Rating from Vivino")
    description: Optional[str] = None
    color: Optional[str] = None
    grape_variety: Optional[str] = None
    alcohol_percentage: Optional[float] = Field(None, ge=0, le=100, description="Alcohol percentage")
    price: Optional[Decimal] = Field(None, ge=0, description="Price of the wine")
    sku: Optional[str] = Field(None, description="Stock Keeping Unit")
    is_active: bool = True


class WineCreate(WineBase):
    pass


class WineUpdate(BaseModel):
    name: Optional[str] = None
    producer: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    volume_ml: Optional[int] = Field(None, gt=0)
    vintage_year: Optional[int] = Field(None, ge=1800, le=2100)
    glasses_per_bottle: Optional[int] = Field(None, gt=0)
    type: Optional[WineType] = None
    rating: Optional[float] = Field(None, ge=0, le=10)
    description: Optional[str] = None
    color: Optional[str] = None
    grape_variety: Optional[str] = None
    alcohol_percentage: Optional[float] = Field(None, ge=0, le=100)
    price: Optional[Decimal] = Field(None, ge=0)
    sku: Optional[str] = None
    is_active: Optional[bool] = None


class Wine(WineBase):
    id: int
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class InventoryBase(BaseModel):
    wine_id: int
    location_type: LocationType
    bottles_count: float = Field(default=0.0, ge=0, description="Number of bottles in inventory (can be fractional)")


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    bottles_count: Optional[float] = Field(None, ge=0)


class Inventory(InventoryBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    # Include wine information in the response
    wine: Optional[Wine] = None

    class Config:
        from_attributes = True


class SaleBase(BaseModel):
    wine_id: int
    sale_type: SaleType
    quantity: float = Field(..., gt=0, description="Number of bottles or glasses sold")
    unit_price: Decimal = Field(..., ge=0, description="Price per unit")
    location_type: LocationType
    notes: Optional[str] = None


class SaleCreate(SaleBase):
    pass


class SaleUpdate(BaseModel):
    notes: Optional[str] = None


class Sale(SaleBase):
    id: int
    total_amount: Decimal
    sale_date: datetime

    # Include wine information in the response
    wine: Optional[Wine] = None

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    wine_id: int
    quantity: int = Field(default=1, gt=0)
    unit_price: Decimal = Field(..., ge=0)


class OrderItemCreate(OrderItemBase):
    pass


class OrderItem(OrderItemBase):
    id: int
    total_price: Decimal

    # Include wine information in the response
    wine: Optional[Wine] = None

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    shipping_address: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    notes: Optional[str] = None


class OrderCreate(OrderBase):
    order_items: List[OrderItemCreate]


class OrderUpdate(BaseModel):
    status: Optional[str] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None


class Order(OrderBase):
    id: int
    uuid: str
    total_amount: Decimal
    shipping_cost: Decimal
    status: str
    payment_method: Optional[str] = None
    payment_status: str
    order_date: datetime
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    notes: Optional[str] = None

    # Include order items in the response
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True


class AdjustmentBase(BaseModel):
    wine_id: int
    location_type: LocationType
    adjustment_type: str = Field(..., description="Type of adjustment: addition, removal, damage")
    quantity: float = Field(..., description="Quantity to adjust (positive for addition, negative for removal)")
    reason: Optional[str] = Field(None, description="Reason for the adjustment")
    adjusted_by: Optional[str] = Field(None, description="Who made the adjustment")
    notes: Optional[str] = None


class AdjustmentCreate(AdjustmentBase):
    pass


class Adjustment(AdjustmentBase):
    id: int
    adjustment_date: datetime

    # Include wine information in the response
    wine: Optional[Wine] = None

    class Config:
        from_attributes = True


class InventoryWithWineDetails(BaseModel):
    """Schema for inventory with wine details and calculated values"""
    id: int
    wine_id: int
    location_type: LocationType
    bottles_count: float
    glasses_count: float  # bottles_count * glasses_per_bottle
    
    # Wine details
    wine_name: str
    wine_producer: str
    wine_country: str
    wine_region: str
    wine_vintage_year: int
    wine_glasses_per_bottle: int
    
    class Config:
        from_attributes = True


class SaleSummary(BaseModel):
    """Schema for aggregated sales data"""
    wine_id: int
    wine_name: str
    vintage_year: int
    total_sold_bottles: float
    total_sold_glasses: float
    total_revenue: Decimal
    location_type: LocationType
    
    class Config:
        from_attributes = True