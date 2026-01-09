from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Date, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@database:5432/wine_shop")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Product model
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    category = Column(String(100))
    producer = Column(String(255))
    country = Column(String(100))
    region = Column(String(100))
    vintage = Column(Integer)  # Year of production
    price = Column(Float(precision=10, scale=2))
    product_type = Column(String(50), default='bottle')  # 'bottle' or 'glass'
    description = Column(Text)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventory_items = relationship("Inventory", back_populates="product")
    sales_records = relationship("Sale", back_populates="product")

# Inventory model
class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    location = Column(String(100))  # Where the inventory is stored (cellar A, cellar B, etc.)
    current_stock = Column(Integer, default=0)
    reserved_stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    product = relationship("Product", back_populates="inventory_items")

# Sale model
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    customer_name = Column(String(255))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float(precision=10, scale=2))
    total_price = Column(Float(precision=10, scale=2))
    sale_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50), default='completed')  # 'completed', 'pending', 'cancelled'

    # Relationship
    product = relationship("Product", back_populates="sales_records")

# Promotion model
class Promotion(Base):
    __tablename__ = "promotions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(100), nullable=False)  # 'five_plus_one', 'free_shipping', 'percentage_discount', 'fixed_discount'
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    active = Column(Boolean, default=True)
    conditions = Column(JSON)  # Store specific conditions for each promotion type
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Inventory Adjustment model
class InventoryAdjustment(Base):
    __tablename__ = "inventory_adjustments"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    old_stock = Column(Integer)
    new_stock = Column(Integer)
    adjustment_reason = Column(String(100))  # 'count_correction', 'breakage', 'tasting', 'other'
    notes = Column(Text)
    adjusted_by = Column(String(255))
    adjusted_at = Column(DateTime, default=datetime.utcnow)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()