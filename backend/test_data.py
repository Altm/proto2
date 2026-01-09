"""
Script to populate the database with test data for the wine inventory management system
"""
from sqlalchemy.orm import Session
from decimal import Decimal
from faker import Faker
import random
from app.database import SessionLocal, init_db
from app.models import Wine, Inventory, Sale, Order, OrderItem, Adjustment
from app.schemas import WineType, LocationType, SaleType


fake = Faker('en_US')


def create_test_data(db: Session):
    """
    Create test data for the wine inventory management system
    """
    print("Creating test data...")
    
    # Create test wines (10 wines with different vintage years)
    wines_data = [
        {
            "name": "Château Margaux",
            "producer": "Château Margaux",
            "country": "France",
            "region": "Bordeaux",
            "volume_ml": 750,
            "vintage_year": 2018,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.8,
            "description": "A prestigious red wine from Bordeaux, France",
            "color": "Red",
            "grape_variety": "Cabernet Sauvignon, Merlot",
            "alcohol_percentage": 13.5,
            "price": Decimal("250.00"),
            "sku": "CM-2018-750"
        },
        {
            "name": "Château Margaux",
            "producer": "Château Margaux",
            "country": "France",
            "region": "Bordeaux",
            "volume_ml": 750,
            "vintage_year": 2019,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.9,
            "description": "Another excellent vintage from Château Margaux",
            "color": "Red",
            "grape_variety": "Cabernet Sauvignon, Merlot",
            "alcohol_percentage": 13.7,
            "price": Decimal("275.00"),
            "sku": "CM-2019-750"
        },
        {
            "name": "Domaine de la Romanée-Conti",
            "producer": "Domaine de la Romanée-Conti",
            "country": "France",
            "region": "Burgundy",
            "volume_ml": 750,
            "vintage_year": 2017,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 5.0,
            "description": "One of the world's most prestigious Pinot Noir wines",
            "color": "Red",
            "grape_variety": "Pinot Noir",
            "alcohol_percentage": 14.0,
            "price": Decimal("15000.00"),
            "sku": "DRC-2017-750"
        },
        {
            "name": "Opus One",
            "producer": "Opus One Winery",
            "country": "USA",
            "region": "Napa Valley",
            "volume_ml": 750,
            "vintage_year": 2018,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.7,
            "description": "Iconic Napa Valley Bordeaux-style blend",
            "color": "Red",
            "grape_variety": "Cabernet Sauvignon, Merlot, Cabernet Franc, Petit Verdot, Malbec",
            "alcohol_percentage": 14.5,
            "price": Decimal("394.00"),
            "sku": "OO-2018-750"
        },
        {
            "name": "Screaming Eagle",
            "producer": "Screaming Eagle",
            "country": "USA",
            "region": "Napa Valley",
            "volume_ml": 750,
            "vintage_year": 2016,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.9,
            "description": "Extremely rare and expensive cult wine from Napa Valley",
            "color": "Red",
            "grape_variety": "Cabernet Sauvignon, Merlot, Cabernet Franc",
            "alcohol_percentage": 15.2,
            "price": Decimal("3500.00"),
            "sku": "SE-2016-750"
        },
        {
            "name": "Champagne Dom Pérignon",
            "producer": "Moët & Chandon",
            "country": "France",
            "region": "Champagne",
            "volume_ml": 750,
            "vintage_year": 2012,
            "glasses_per_bottle": 6,
            "type": WineType.SPARKLING,
            "rating": 4.6,
            "description": "Luxury champagne named after its legendary creator",
            "color": "Sparkling",
            "grape_variety": "Pinot Noir, Chardonnay",
            "alcohol_percentage": 12.5,
            "price": Decimal("250.00"),
            "sku": "DP-2012-750"
        },
        {
            "name": "Chablis Grand Cru Les Clos",
            "producer": "William Fèvre",
            "country": "France",
            "region": "Burgundy",
            "volume_ml": 750,
            "vintage_year": 2019,
            "glasses_per_bottle": 5,
            "type": WineType.WHITE,
            "rating": 4.5,
            "description": "Exceptional Chablis Grand Cru from the historic Les Clos vineyard",
            "color": "White",
            "grape_variety": "Chardonnay",
            "alcohol_percentage": 13.0,
            "price": Decimal("150.00"),
            "sku": "CGLC-2019-750"
        },
        {
            "name": "Sauternes Château d'Yquem",
            "producer": "Château d'Yquem",
            "country": "France",
            "region": "Bordeaux",
            "volume_ml": 375,
            "vintage_year": 2015,
            "glasses_per_bottle": 8,
            "type": WineType.DESSERT,
            "rating": 4.9,
            "description": "World-renowned sweet wine from Sauternes",
            "color": "Sweet White",
            "grape_variety": "Sémillon, Sauvignon Blanc",
            "alcohol_percentage": 14.0,
            "price": Decimal("550.00"),
            "sku": "CY-2015-375"
        },
        {
            "name": "Barolo Cannubi",
            "producer": "Gaja",
            "country": "Italy",
            "region": "Piedmont",
            "volume_ml": 750,
            "vintage_year": 2016,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.8,
            "description": "Powerful Nebbiolo from the legendary Cannubi vineyard",
            "color": "Red",
            "grape_variety": "Nebbiolo",
            "alcohol_percentage": 14.5,
            "price": Decimal("350.00"),
            "sku": "BC-2016-750"
        },
        {
            "name": "Rioja Gran Reserva",
            "producer": "Marqués de Riscal",
            "country": "Spain",
            "region": "Rioja",
            "volume_ml": 750,
            "vintage_year": 2010,
            "glasses_per_bottle": 5,
            "type": WineType.RED,
            "rating": 4.4,
            "description": "Exceptionally aged Rioja with complex flavors",
            "color": "Red",
            "grape_variety": "Tempranillo, Garnacha",
            "alcohol_percentage": 13.5,
            "price": Decimal("85.00"),
            "sku": "RGR-2010-750"
        }
    ]
    
    created_wines = []
    for wine_data in wines_data:
        wine = Wine(**wine_data)
        db.add(wine)
        created_wines.append(wine)
    
    db.commit()
    
    # Create inventory for each wine at both locations
    for wine in created_wines:
        # Warehouse inventory
        warehouse_inventory = Inventory(
            wine_id=wine.id,
            location_type=LocationType.WAREHOUSE,
            bottles_count=random.randint(5, 20)  # Random stock between 5-20 bottles
        )
        db.add(warehouse_inventory)
        
        # Bar/Restaurant inventory
        bar_inventory = Inventory(
            wine_id=wine.id,
            location_type=LocationType.BAR_RESTAURANT,
            bottles_count=random.randint(2, 8)  # Random stock between 2-8 bottles
        )
        db.add(bar_inventory)
    
    db.commit()
    
    # Create some sales records
    for _ in range(15):  # Create 15 sales
        wine = random.choice(created_wines)
        sale_type = random.choice([SaleType.BOTTLE, SaleType.GLASS])
        
        if sale_type == SaleType.BOTTLE:
            quantity = random.randint(1, 3)
            unit_price = wine.price
        else:  # Glass
            quantity = random.randint(1, 5)
            unit_price = Decimal(str(float(wine.price) / wine.glasses_per_bottle * 1.5))  # Price per glass with markup
        
        total_amount = quantity * unit_price
        
        sale = Sale(
            wine_id=wine.id,
            sale_type=sale_type,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
            location_type=random.choice([LocationType.WAREHOUSE, LocationType.BAR_RESTAURANT]),
            notes=fake.sentence(nb_words=6)
        )
        db.add(sale)
    
    db.commit()
    
    # Create some orders
    for _ in range(8):  # Create 8 orders
        order = Order(
            customer_name=fake.name(),
            customer_email=fake.email(),
            shipping_address=fake.address(),
            postal_code=fake.postcode(),
            country=fake.country(),
            total_amount=Decimal("0.00"),  # Will be calculated after adding items
            shipping_cost=Decimal(str(random.uniform(10, 50))),
            status=random.choice(["pending", "paid", "shipped", "delivered"]),
            payment_method=random.choice(["stripe", "paypal"]),
            payment_status=random.choice(["pending", "succeeded", "failed"]),
            notes=fake.sentence(nb_words=8)
        )
        db.add(order)
        db.flush()  # Get the order ID without committing
        
        # Add random items to the order
        num_items = random.randint(1, 3)
        order_total = Decimal("0.00")
        
        for _ in range(num_items):
            wine = random.choice(created_wines)
            quantity = random.randint(1, 2)
            unit_price = wine.price
            total_price = quantity * unit_price
            
            order_item = OrderItem(
                order_id=order.id,
                wine_id=wine.id,
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price
            )
            db.add(order_item)
            order_total += total_price
        
        # Update the order total
        order.total_amount = order_total + order.shipping_cost
        db.merge(order)
    
    db.commit()
    
    # Create some inventory adjustments
    for _ in range(10):  # Create 10 adjustments
        wine = random.choice(created_wines)
        location_type = random.choice([LocationType.WAREHOUSE, LocationType.BAR_RESTAURANT])
        
        adjustment = Adjustment(
            wine_id=wine.id,
            location_type=location_type,
            adjustment_type=random.choice(["addition", "removal", "damage"]),
            quantity=random.choice([-5, -3, -1, 1, 3, 5, 10]),  # Positive for additions, negative for removals
            reason=random.choice([
                "New shipment received",
                "Inventory count correction", 
                "Damaged goods",
                "Transfer between locations",
                "Tasting samples"
            ]),
            adjusted_by=fake.name(),
            notes=fake.sentence(nb_words=6)
        )
        db.add(adjustment)
    
    db.commit()
    
    print(f"Created {len(created_wines)} wines, inventory entries, sales, orders, and adjustments")


if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Clear existing data (optional - comment out if you want to keep existing data)
        db.query(Adjustment).delete()
        db.query(OrderItem).delete()
        db.query(Order).delete()
        db.query(Sale).delete()
        db.query(Inventory).delete()
        db.query(Wine).delete()
        
        # Create new test data
        create_test_data(db)
        
        print("Test data created successfully!")
    except Exception as e:
        print(f"Error creating test data: {e}")
        db.rollback()
    finally:
        db.close()