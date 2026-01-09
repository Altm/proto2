"""
Database models for the wine inventory management system
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, ForeignKey, Enum, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from datetime import datetime
from uuid import uuid4

Base = declarative_base()


class WineType(enum.Enum):
    RED = "red"
    WHITE = "white"
    ROSE = "rose"
    SPARKLING = "sparkling"
    DESSERT = "dessert"
    FORTIFIED = "fortified"


class LocationType(enum.Enum):
    WAREHOUSE = "warehouse"
    BAR_RESTAURANT = "bar_restaurant"


class SaleType(enum.Enum):
    BOTTLE = "bottle"
    GLASS = "glass"


class Wine(Base):
    __tablename__ = "wines"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid4()), index=True)
    name = Column(String, nullable=False)
    producer = Column(String, nullable=False)  # winery
    country = Column(String, nullable=False)
    region = Column(String, nullable=False)
    volume_ml = Column(Integer, nullable=False)  # bottle volume in ml
    vintage_year = Column(Integer, nullable=False)  # year of production
    glasses_per_bottle = Column(Integer, default=5, nullable=False)  # number of glasses per bottle
    type = Column(Enum(WineType), nullable=True)
    rating = Column(Float, nullable=True)  # from Vivino
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)
    grape_variety = Column(String, nullable=True)
    alcohol_percentage = Column(Float, nullable=True)
    price = Column(Numeric(10, 2), nullable=True)
    sku = Column(String, nullable=True)  # Stock Keeping Unit
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    inventory_items = relationship("Inventory", back_populates="wine")
    sales = relationship("Sale", back_populates="wine")


class Inventory(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)  # warehouse or bar/restaurant
    bottles_count = Column(Float, default=0.0, nullable=False)  # can be fractional for glasses
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    wine = relationship("Wine", back_populates="inventory_items")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    sale_type = Column(Enum(SaleType), nullable=False)  # bottle or glass
    quantity = Column(Float, nullable=False)  # number of bottles or glasses sold
    unit_price = Column(Numeric(10, 2), nullable=False)  # price per unit
    total_amount = Column(Numeric(10, 2), nullable=False)  # total sale amount
    location_type = Column(Enum(LocationType), nullable=False)  # where the sale happened
    sale_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    # Relationships
    wine = relationship("Wine", back_populates="sales")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, default=lambda: str(uuid4()), index=True)
    customer_name = Column(String, nullable=True)
    customer_email = Column(String, nullable=True)
    shipping_address = Column(Text, nullable=True)
    postal_code = Column(String, nullable=True)
    country = Column(String, nullable=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    shipping_cost = Column(Numeric(10, 2), default=0.0)
    status = Column(String, default="pending")  # pending, paid, shipped, delivered, cancelled
    payment_method = Column(String, nullable=True)  # stripe, paypal
    payment_status = Column(String, default="pending")  # pending, succeeded, failed, refunded
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    notes = Column(Text, nullable=True)

    # Relationships
    order_items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)

    # Relationships
    order = relationship("Order", back_populates="order_items")
    wine = relationship("Wine")


class Adjustment(Base):
    __tablename__ = "adjustments"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    location_type = Column(Enum(LocationType), nullable=False)
    adjustment_type = Column(String, nullable=False)  # addition, removal, damage
    quantity = Column(Float, nullable=False)  # positive for addition, negative for removal
    reason = Column(String, nullable=True)  # reason for adjustment
    adjusted_by = Column(String, nullable=True)  # who made the adjustment
    adjustment_date = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text, nullable=True)

    # Relationships
    wine = relationship("Wine")


class VivinoMapping(Base):
    __tablename__ = "vivino_mappings"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    vivino_id = Column(String, nullable=False)  # ID from Vivino API
    vivino_url = Column(String, nullable=True)
    last_synced = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    wine = relationship("Wine")


class ShopifySync(Base):
    __tablename__ = "shopify_syncs"

    id = Column(Integer, primary_key=True, index=True)
    wine_id = Column(Integer, ForeignKey("wines.id"), nullable=False)
    shopify_product_id = Column(String, nullable=False)  # ID from Shopify
    shopify_variant_id = Column(String, nullable=True)  # Variant ID that includes vintage year
    last_synced = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    wine = relationship("Wine")