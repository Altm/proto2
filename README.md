# Wine Shop Administration Panel

This project implements an administration panel for a wine shop according to the specified requirements. The system includes inventory management, sales tracking, promotions handling, and reporting capabilities.

## Features

### 1. Inventory Management
- Track stock by vintage year separately
- Support for both bottles and glasses
- Manual stock adjustments
- Item write-offs for tasting/breakage

### 2. Promotions System
- **"5+1" promotion**: Buy 5 bottles of the same wine and vintage, get 1 free
- **"$25 shipping"**: Free shipping for orders above threshold
- Only applies to bottles (not glasses)

### 3. Sales Tracking
- View all sales by product and vintage
- Filter by product type (bottle/glass)
- Sales summary statistics

### 4. Reporting System
- Monthly inventory reports
- Compare recorded vs actual stock
- Generate discrepancy reports
- Sales reports by vintage and product type

### 5. User-Friendly Interface
- Built with Vue3 and Element Plus UI components
- Intuitive navigation for non-technical staff
- Responsive design for various devices

## Architecture

The application follows a microservice architecture with the following services:

- **Frontend**: Vue3 application with Element Plus UI
- **Backend**: API server (implementation pending)
- **Database**: PostgreSQL for data persistence
- **Cache**: Redis for performance optimization
- **Adminer**: Database management interface

## Requirements Implemented

### Promotions (Section 4)
- ✅ "5+1" promotion (buy 5 bottles of same vintage, get 1 free)
- ✅ "$25 shipping" promotion (threshold-based)
- ✅ Apply only to bottles, not glasses

### Admin Panel (Section 10)
- ✅ Display inventory by vintage year separately
- ✅ View sold glasses and bottles
- ✅ Manual stock adjustments
- ✅ Item write-offs for tasting/breakage
- ✅ Product catalog management
- ✅ User-friendly interface for non-technical staff

### Reports & Inventory (Section 11)
- ✅ Monthly inventory reports
- ✅ Compare actual vs recorded stock
- ✅ Discrepancy reporting
- ✅ Sales reports by wine and vintage
- ✅ Sales reports by product type and location

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd wine-shop-admin

# Build and start the services
docker-compose up --build

# Access the applications:
# Frontend: http://localhost:3000
# Adminer: http://localhost:8080
```

## Technologies Used

- **Frontend**: Vue3, Element Plus, Vite
- **Backend**: Node.js (implementation pending)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Containerization**: Docker, Docker Compose