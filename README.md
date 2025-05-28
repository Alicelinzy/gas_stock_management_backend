# Gas Stock Management Backend

## Overview

A Django REST API for managing gas stock, orders, invoices, payments, and user roles (Buyer, Seller, Admin). Built with PostgreSQL, JWT authentication, and Docker support. This backend serves both web and mobile clients.

---

## Features

* Role-based access: Buyer, Seller, Admin
* Gas inventory management
* Order processing and approval
* Invoice and payment workflows
* Ratings and feedback system
* RESTful API with JWT authentication

---

## Tech Stack

* **Framework:** Django REST Framework
* **Database:** PostgreSQL
* **Auth:** JWT-based
* **Environment:** Dockerized
* **API Format:** JSON over HTTP

---

## User Roles

| Role   | Capabilities                                              |
| ------ | --------------------------------------------------------- |
| Buyer  | Browse gas stock, place orders, submit ratings & feedback |
| Seller | Manage inventory, process orders, submit invoices         |
| Admin  | Approve orders/invoices, manage payments & deliveries     |

---

## API Overview

### Auth

* `POST /api/v1/register/` — Register (Buyer/Seller/Admin)
* `POST /api/v1/login/` — JWT token login

### Inventory

* `GET /api/v1/gas/` — List inventory (filters: brand, weight, location)
* `GET /api/v1/seller/inventory/` — View seller's inventory
* `POST /api/inventory/` — Add new inventory
* `PATCH /api/inventory/{id}/` — Update inventory

### Orders

* `POST /api/v1/orders/` — Place an order (Buyer)
* `GET /api/orders/my_orders/` — View buyer's orders
* `GET /api/v1/seller/orders/` — View seller orders
* `POST /api/orders/{id}/approve/` — Approve (Admin)
* `POST /api/orders/{id}/reject/` — Reject (Admin)
* `POST /api/orders/{id}/cancel/` — Cancel (Buyer)
* `POST /api/orders/{id}/mark-delivered/` — Mark delivered (Seller)

### Invoices & Payments

* `POST /api/v1/seller/invoice/` — Submit invoice (Seller)
* `GET /api/v1/admin/invoices/pending/` — Pending invoices (Admin)
* `POST /api/invoices/{id}/approve/` — Approve invoice (Admin)
* `POST /api/invoices/{id}/mark-as-paid/` — Mark as paid (Admin)

### Feedback

* `POST /api/v1/feedback/` — Submit rating (Buyer)
* `GET /api/ratings/` — View ratings

---

## Setup Guide

### Prerequisites

* Docker & Docker Compose
* Git

### 1. Clone & Configure

```bash
git clone https://github.com/Alicelinzy/gas_stock_management_backend.git
cd gas_stock_management_backend
cp .env.example .env
```

> Edit `.env` with your DB credentials and JWT secret.

### 2. Run the App

```bash
docker-compose up --build
```

### 3. Create Admin User

```bash
docker-compose exec web python manage.py createsuperuser
```

### 4. Access Services

* API: `http://localhost:8000/api/`
* Admin: `http://localhost:8000/admin/`
* DB: PostgreSQL on `localhost:5432`

---

## Environment Variables

`.env` example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=gas_management_db
DB_USER=postgres
DB_PASSWORD=your-db-password
DB_HOST=db
DB_PORT=5432

JWT_SECRET_KEY=your-jwt-secret
```

---

## Developer Guide

### Common Commands

```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create new migration
docker-compose exec web python manage.py makemigrations

# Access Django shell
docker-compose exec web python manage.py shell

# Run tests
docker-compose exec web python manage.py test
```

### Rebuild Project

```bash
# Code changes
docker-compose restart web

# Dependency changes
docker-compose up --build web

# Docker config changes
docker-compose down
docker-compose up --build
```

---

## Database Models

### Core Models

* `User` & `UserProfile` — with roles: Buyer, Seller, Admin
* `GasInventory` — seller-managed stock
* `Order` — buyer orders linked to inventory
* `Invoice` & `Payment` — order billing and transactions
* `Rating` — buyer feedback

### Relations Overview

```
User ←→ UserProfile
User ←→ GasInventory (as Seller)
User ←→ Order (as Buyer)
GasInventory ←→ Order
Order ←→ Invoice ←→ Payment
Order ←→ Rating
```

---

## Testing Flow

1. Register Buyer, Seller, and Admin
2. Login and retrieve JWTs
3. Seller adds inventory
4. Buyer places order
5. Admin approves order
6. Seller marks as delivered
7. Seller submits invoice
8. Admin approves invoice and marks paid
9. Buyer submits rating

---

## Troubleshooting

### Common Fixes

**Port Conflict**

```bash
# Change port in docker-compose.yml
docker-compose down
docker-compose up -d
```

**Permissions**

```bash
sudo chown -R $USER:$USER .
```

**Reset Database**

```bash
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

---

## Production Notes

### Setup

* Set `DEBUG=False`, strong `SECRET_KEY`, and proper `ALLOWED_HOSTS`
* Use `docker-compose.prod.yml` for production builds

```bash
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### Security

* Configure HTTPS
* Use environment variables for secrets
* Setup firewalls and logging
* Enable automatic backups

---

## Contributing

### Code Style

* Follow PEP 8
* Write docstrings
* Cover features with tests
* Keep API docs updated

### Git Workflow

```bash
git checkout -b feature/your-feature-name
# Make changes and test
git commit -m "Add your message"
git push origin feature/your-feature-name
```
