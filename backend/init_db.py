"""Database initialization script"""

from database import engine, Base
from sqlalchemy.orm import sessionmaker
from database import Product, Inventory, Promotion

def init_db():
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Check if we already have data
    existing_products = session.query(Product).first()
    
    if not existing_products:
        print("Adding initial data...")
        
        # Add some sample products
        products_data = [
            {
                "name": "Château Margaux 2018",
                "category": "red_wine",
                "producer": "Château Margaux",
                "country": "France",
                "region": "Bordeaux",
                "vintage": 2018,
                "price": 450.00,
                "product_type": "bottle",
                "description": "Premium red wine from Bordeaux"
            },
            {
                "name": "Château Margaux 2017",
                "category": "red_wine",
                "producer": "Château Margaux",
                "country": "France",
                "region": "Bordeaux",
                "vintage": 2017,
                "price": 380.00,
                "product_type": "bottle",
                "description": "Red wine from Bordeaux"
            },
            {
                "name": "Dom Pérignon 2016",
                "category": "sparkling",
                "producer": "Moët & Chandon",
                "country": "France",
                "region": "Champagne",
                "vintage": 2016,
                "price": 220.00,
                "product_type": "bottle",
                "description": "Luxury champagne"
            },
            {
                "name": "Champagne Glass Set",
                "category": "glassware",
                "producer": "Riedel",
                "country": "Austria",
                "region": "Kufstein",
                "vintage": None,
                "price": 85.00,
                "product_type": "glass",
                "description": "Set of 6 champagne glasses"
            }
        ]
        
        for prod_data in products_data:
            product = Product(**prod_data)
            session.add(product)
        
        # Add corresponding inventory
        for i, prod_data in enumerate(products_data, 1):
            inventory = Inventory(
                product_id=i,
                location="Cellar A" if i <= 2 else "Cellar B" if i == 3 else "Bar",
                current_stock=20,
                reserved_stock=0
            )
            session.add(inventory)
        
        # Add some promotions
        five_plus_one_promo = Promotion(
            name="5+1 Free Promotion",
            type="five_plus_one",
            description="Buy 5 bottles of the same wine and vintage, get 1 free",
            start_date="2023-01-01",
            end_date="2024-12-31",
            active=True,
            conditions={
                "vintage_years": [2015, 2016, 2017, 2018],
                "product_ids": [1, 2, 3]
            }
        )
        
        shipping_promo = Promotion(
            name="Free Shipping over $25",
            type="free_shipping",
            description="Free shipping for orders over $25",
            start_date="2023-01-01",
            end_date="2024-12-31",
            active=True,
            conditions={
                "min_order_amount": 25.00
            }
        )
        
        session.add(five_plus_one_promo)
        session.add(shipping_promo)
        
        # Commit all changes
        session.commit()
        print("Initial data added successfully!")
    else:
        print("Database already initialized.")
    
    session.close()

if __name__ == "__main__":
    init_db()