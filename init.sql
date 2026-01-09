-- Initial database setup for wine inventory system
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Additional extensions that might be needed
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For similarity searches
CREATE EXTENSION IF NOT EXISTS "unaccent"; -- For accent-insensitive searches