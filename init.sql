-- Initial database schema for wine shop

-- Create products table
CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    producer VARCHAR(255),
    country VARCHAR(100),
    region VARCHAR(100),
    vintage INTEGER,
    price DECIMAL(10,2),
    product_type VARCHAR(50) DEFAULT 'bottle', -- 'bottle' or 'glass'
    description TEXT,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create inventory table
CREATE TABLE IF NOT EXISTS inventory (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    location VARCHAR(100),
    current_stock INTEGER DEFAULT 0,
    reserved_stock INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create sales table
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    customer_name VARCHAR(255),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'completed' -- 'completed', 'pending', 'cancelled'
);

-- Create promotions table
CREATE TABLE IF NOT EXISTS promotions (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL, -- 'five_plus_one', 'free_shipping', 'percentage_discount', 'fixed_discount'
    description TEXT,
    start_date DATE,
    end_date DATE,
    active BOOLEAN DEFAULT true,
    conditions JSONB, -- Store specific conditions for each promotion type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create inventory adjustments table
CREATE TABLE IF NOT EXISTS inventory_adjustments (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id),
    old_stock INTEGER,
    new_stock INTEGER,
    adjustment_reason VARCHAR(100), -- 'count_correction', 'breakage', 'tasting', 'other'
    notes TEXT,
    adjusted_by VARCHAR(255),
    adjusted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data
INSERT INTO products (name, category, producer, country, region, vintage, price, product_type, description) VALUES
('Château Margaux 2018', 'red_wine', 'Château Margaux', 'France', 'Bordeaux', 2018, 450.00, 'bottle', 'Premium red wine from Bordeaux'),
('Château Margaux 2017', 'red_wine', 'Château Margaux', 'France', 'Bordeaux', 2017, 380.00, 'bottle', 'Red wine from Bordeaux'),
('Dom Pérignon 2016', 'sparkling', 'Moët & Chandon', 'France', 'Champagne', 2016, 220.00, 'bottle', 'Luxury champagne'),
('Opus One 2017', 'red_wine', 'Opus One Winery', 'USA', 'Napa Valley', 2017, 320.00, 'bottle', 'Napa Valley premium blend'),
('Screaming Eagle Cabernet 2015', 'red_wine', 'Screaming Eagle', 'USA', 'Napa Valley', 2015, 2500.00, 'bottle', 'Rare Napa Valley Cabernet Sauvignon'),
('Champagne Glass Set', 'glassware', 'Riedel', 'Austria', 'Kufstein', NULL, 85.00, 'glass', 'Set of 6 champagne glasses'),
('Wine Tasting Glass Set', 'glassware', 'Schott Zwiesel', 'Germany', 'Bavaria', NULL, 65.00, 'glass', 'Set of 6 wine tasting glasses');

-- Insert sample inventory records
INSERT INTO inventory (product_id, location, current_stock, reserved_stock) VALUES
(1, 'Cellar A', 45, 5),
(2, 'Cellar A', 32, 3),
(3, 'Cellar B', 28, 2),
(4, 'Cellar A', 15, 0),
(5, 'VIP Room', 8, 1),
(6, 'Bar', 42, 0),
(7, 'Tasting Room', 30, 0);

-- Insert sample promotions
INSERT INTO promotions (name, type, description, start_date, end_date, active, conditions) VALUES
('5+1 Free Promotion', 'five_plus_one', 'Buy 5 bottles of the same wine and vintage, get 1 free', '2023-01-01', '2023-12-31', true, '{"vintage_years": [2015, 2016, 2017, 2018], "product_ids": [1, 2, 3]}'),
('Free Shipping over $25', 'free_shipping', 'Free shipping for orders over $25', '2023-01-01', '2023-12-31', true, '{"min_order_amount": 25.00}');