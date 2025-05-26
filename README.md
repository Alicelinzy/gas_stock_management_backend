# Gas Stock Management Backend

## Overview

This backend powers the **Gas Stock Management System**, managing gas inventory, orders, invoices, payments, and user roles (Buyer, Seller, Admin). It exposes a RESTful API for frontend and mobile applications to interact with.

---

## Architecture

* **Framework:** Django REST Framework (DRF)
* **Database:** PostgreSQL (recommended for relational data integrity)
* **Authentication:** JWT Token-based
* **API Format:** JSON over HTTP
* **Environment:** Dockerized (optional but recommended for development)

---

## User Roles & Capabilities

| Role   | Main Responsibilities                                            |
| ------ | ---------------------------------------------------------------- |
| Buyer  | Browse/filter gas stock, place orders, submit feedback           |
| Seller | Manage inventory, receive orders, generate invoices              |
| Admin  | Approve orders and invoices, manage payments, authorize delivery |

---

## API Structure

### Authentication

* `POST /api/v1/register` — Register new user (Buyer or Seller)
* `POST /api/v1/login` — Login and receive JWT token
* `POST /api/v1/logout` — Logout and revoke token

### Buyer Endpoints

* `GET /api/v1/gas` — List available gas inventory

  * Supports filters: `brand`, `weight`, `location`
  * Example: `/api/v1/gas?brand=Jibu&weight=12kg&location=Kigali`

* `POST /api/v1/orders` — Place a new order

* `POST /api/v1/feedback` — Submit feedback and rating for a seller

### Seller Endpoints

* `GET /api/v1/seller/inventory` — View and manage current gas stock

* `POST /api/v1/seller/inventory` — Add or update stock

* `GET /api/v1/seller/orders` — View orders assigned to the seller

* `POST /api/v1/seller/invoice` — Submit invoice for order delivery

### Admin Endpoints

* `GET /api/v1/admin/orders/pending` — View orders waiting for approval

* `PATCH /api/v1/admin/orders/:id/approve` — Approve or reject orders

* `GET /api/v1/admin/invoices/pending` — View invoices pending approval

* `PATCH /api/v1/admin/invoices/:id/approve` — Approve invoices

* `PATCH /api/v1/admin/delivery/:id/confirm` — Confirm delivery and release payment

---

## Database Models (Simplified)

* **User:** Stores user info and role (buyer, seller, admin)
* **GasInventory:** Tracks seller’s gas stock by brand, weight, quantity, and location
* **Orders:** Records buyer orders linked to seller inventory
* **Invoices:** Tracks invoice status for orders
* **Feedback:** Buyers rate and comment on sellers
* **Payments:** Manages payment records from admin to seller

---

## How to Use This Backend

1. **Frontend & Mobile developers:**

   * Use the REST API endpoints to implement:

     * Gas browsing & filtering UI
     * Order placement flows
     * Invoice viewing & confirmation (for sellers)
     * Admin dashboards for order & invoice approvals
     * Feedback and rating forms

   * Use JWT authentication for secure API calls.

2. **Backend developers:**

   * Follow the established models and serializers in `models.py` and `serializers.py`.
   * Write views using Django REST Framework's class-based views or viewsets.
   * Add permissions to ensure role-based access.
   * Implement signals to automate notifications on order status changes.
   * Write unit and integration tests to ensure API stability.

3. **General development tips:**

   * Run migrations whenever models change: `python manage.py migrate`
   * Use Django admin for quick data inspection during development.
   * Document any API changes here and keep the OpenAPI/Swagger docs updated.

---

## Development Environment Setup

1. Clone the repo
2. Create a virtual environment
3. Install dependencies
4. Set up `.env` with database credentials and secret keys
5. Run migrations and seed initial data
6. Run the development server