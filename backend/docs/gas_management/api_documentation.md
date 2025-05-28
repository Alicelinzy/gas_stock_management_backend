# Gas Stock Management API Documentation

This document provides a comprehensive overview of the Gas Stock Management API endpoints, their functionality, request/response formats, and authentication requirements.

## Table of Contents

1. [Authentication](#authentication)
   - [Register](#register)
   - [Login](#login)
2. [User Profile](#user-profile)
   - [Get Current User Profile](#get-current-user-profile)
   - [List All Users](#list-all-users)
3. [Gas Inventory](#gas-inventory)
   - [List All Gas Inventory](#list-all-gas-inventory)
   - [Retrieve Gas Inventory Item](#retrieve-gas-inventory-item)
   - [Create Gas Inventory Item](#create-gas-inventory-item)
   - [Update Gas Inventory Item](#update-gas-inventory-item)
   - [Delete Gas Inventory Item](#delete-gas-inventory-item)
   - [My Inventory (Seller)](#my-inventory-seller)
4. [Orders](#orders)
   - [List All Orders](#list-all-orders)
   - [Retrieve Order](#retrieve-order)
   - [Create Order](#create-order)
   - [Update Order](#update-order)
   - [Delete Order](#delete-order)
   - [My Orders (Buyer)](#my-orders-buyer)
   - [Seller Orders](#seller-orders)
   - [Approve Order](#approve-order)
   - [Reject Order](#reject-order)
   - [Cancel Order](#cancel-order)
   - [Mark Order as Delivered](#mark-order-as-delivered)
   - [Admin: List Pending Orders](#admin-list-pending-orders)
5. [Invoices](#invoices)
   - [List All Invoices](#list-all-invoices)
   - [Retrieve Invoice](#retrieve-invoice)
   - [Create Invoice](#create-invoice)
   - [Approve Invoice](#approve-invoice)
   - [Mark Invoice as Paid](#mark-invoice-as-paid)
   - [Admin: List Pending Invoices](#admin-list-pending-invoices)
6. [Payments](#payments)
   - [List All Payments](#list-all-payments)
   - [Retrieve Payment](#retrieve-payment)
   - [Create Payment](#create-payment)
   - [Update Payment](#update-payment)
7. [Ratings](#ratings)
   - [List All Ratings](#list-all-ratings)
   - [Retrieve Rating](#retrieve-rating)
   - [Create Rating](#create-rating)

## Authentication

Authentication is managed using JWT (JSON Web Tokens). Include the token in the Authorization header for all authenticated requests:

```
Authorization: Bearer <your_token_here>
```

### Register

Register a new user with a specific role (BUYER, SELLER, or ADMIN).

**Endpoint:** `POST /register/` or `POST /v1/register/`

**Permission:** All users (no authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "securepassword",
  "first_name": "John",
  "last_name": "Doe",
  "role": "BUYER",
  "phone_number": "+1-123-456-7890",
  "address": "123 Main St, Anytown, AN 12345"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "User registered successfully"
}
```

### Login

Authenticate and receive a JWT token.

**Endpoint:** `POST /v1/login/`

**Permission:** All users (no authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```

**Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## User Profile

### Get Current User Profile

Get the profile details of the currently authenticated user.

**Endpoint:** `GET /profiles/me/`

**Permission:** Authenticated users

**Response (200 OK):**
```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "role": "BUYER",
  "phone_number": "+1-123-456-7890",
  "address": "123 Main St, Anytown, AN 12345"
}
```

### List All Users

Get a list of all user profiles.

**Endpoint:** `GET /profiles/`

**Permission:** Authenticated users

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "johndoe@example.com",
      "first_name": "John",
      "last_name": "Doe"
    },
    "role": "BUYER",
    "phone_number": "+1-123-456-7890",
    "address": "123 Main St, Anytown, AN 12345"
  },
  {
    "id": 2,
    "user": {
      "id": 2,
      "username": "janesmith",
      "email": "janesmith@example.com",
      "first_name": "Jane",
      "last_name": "Smith"
    },
    "role": "SELLER",
    "phone_number": "+1-234-567-8901",
    "address": "456 Oak St, Othertown, OT 67890"
  }
]
```

## Gas Inventory

### List All Gas Inventory

Get a list of all available gas inventory items with quantity > 0.

**Endpoint:** `GET /inventory/` or `GET /v1/gas/`

**Permission:** Authenticated users (all roles)

**Query Parameters:**
- `brand` - Filter by gas brand (e.g., JIBU, MERU, TOTAL, OTHER)
- `weight` - Filter by weight in kg
- `location` - Filter by location (substring match)
- `min_price` - Filter by minimum price
- `max_price` - Filter by maximum price
- `seller` - Filter by seller ID

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "brand": "JIBU",
    "weight_kg": 6.0,
    "quantity": 20,
    "unit_price": 2500.0,
    "seller": 2,
    "seller_name": "janesmith",
    "location": "Nairobi",
    "date_added": "2023-06-15T10:30:00Z",
    "last_updated": "2023-06-15T10:30:00Z"
  },
  {
    "id": 2,
    "brand": "MERU",
    "weight_kg": 13.0,
    "quantity": 15,
    "unit_price": 4500.0,
    "seller": 2,
    "seller_name": "janesmith",
    "location": "Mombasa",
    "date_added": "2023-06-16T11:45:00Z",
    "last_updated": "2023-06-16T11:45:00Z"
  }
]
```

### Retrieve Gas Inventory Item

Get details of a specific gas inventory item.

**Endpoint:** `GET /inventory/{id}/`

**Permission:** Authenticated users (all roles)

**Response (200 OK):**
```json
{
  "id": 1,
  "brand": "JIBU",
  "weight_kg": 6.0,
  "quantity": 20,
  "unit_price": 2500.0,
  "seller": 2,
  "seller_name": "janesmith",
  "location": "Nairobi",
  "date_added": "2023-06-15T10:30:00Z",
  "last_updated": "2023-06-15T10:30:00Z"
}
```

### Create Gas Inventory Item

Add a new gas inventory item.

**Endpoint:** `POST /inventory/` or `POST /v1/seller/inventory/`

**Permission:** Authenticated users with SELLER role

**Request Body:**
```json
{
  "brand": "JIBU",
  "weight_kg": 6.0,
  "quantity": 20,
  "unit_price": 2500.0,
  "location": "Nairobi"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "brand": "JIBU",
  "weight_kg": 6.0,
  "quantity": 20,
  "unit_price": 2500.0,
  "seller": 2,
  "seller_name": "janesmith",
  "location": "Nairobi",
  "date_added": "2023-06-15T10:30:00Z",
  "last_updated": "2023-06-15T10:30:00Z"
}
```

### Update Gas Inventory Item

Update an existing gas inventory item.

**Endpoint:** `PUT /inventory/{id}/` or `PATCH /inventory/{id}/`

**Permission:** Authenticated seller who owns the inventory

**Request Body (PUT - complete update):**
```json
{
  "brand": "JIBU",
  "weight_kg": 6.0,
  "quantity": 25,
  "unit_price": 2700.0,
  "location": "Nairobi"
}
```

**Request Body (PATCH - partial update):**
```json
{
  "quantity": 25,
  "unit_price": 2700.0
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "brand": "JIBU",
  "weight_kg": 6.0,
  "quantity": 25,
  "unit_price": 2700.0,
  "seller": 2,
  "seller_name": "janesmith",
  "location": "Nairobi",
  "date_added": "2023-06-15T10:30:00Z",
  "last_updated": "2023-06-17T14:20:00Z"
}
```

### Delete Gas Inventory Item

Remove a gas inventory item.

**Endpoint:** `DELETE /inventory/{id}/`

**Permission:** Authenticated seller who owns the inventory

**Response (204 No Content)**

### My Inventory (Seller)

Get list of inventory items owned by the authenticated seller.

**Endpoint:** `GET /inventory/my_inventory/` or `GET /v1/seller/inventory/`

**Permission:** Authenticated users (all roles, but filters for the authenticated seller)

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "brand": "JIBU",
    "weight_kg": 6.0,
    "quantity": 20,
    "unit_price": 2500.0,
    "seller": 2,
    "seller_name": "janesmith",
    "location": "Nairobi",
    "date_added": "2023-06-15T10:30:00Z",
    "last_updated": "2023-06-15T10:30:00Z"
  }
]
```

## Orders

### List All Orders

Get a list of all orders for the current user.

**Endpoint:** `GET /orders/`

**Permission:** 
- Admin can see all orders
- Buyers can see their own orders
- Sellers can see orders related to their inventory

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "PENDING",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T09:15:00Z"
  }
]
```

### Retrieve Order

Get details of a specific order.

**Endpoint:** `GET /orders/{id}/`

**Permission:** 
- Admin can see any order
- Buyer can see their own orders
- Seller can see orders for their inventory

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "PENDING",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T09:15:00Z"
}
```

### Create Order

Create a new order for gas inventory.

**Endpoint:** `POST /orders/` or `POST /v1/orders/`

**Permission:** Authenticated users with BUYER role

**Request Body:**
```json
{
  "gas_inventory": 1,
  "quantity": 2,
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "PENDING",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T09:15:00Z"
}
```

### Update Order

Update an existing order.

**Endpoint:** `PUT /orders/{id}/` or `PATCH /orders/{id}/`

**Permission:** 
- Buyer can update their own orders (limited fields)
- Admin can update any order

**Request Body (PATCH - partial update):**
```json
{
  "delivery_address": "456 New St, Anytown, AN 12345",
  "contact_phone": "+1-987-654-3210"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "PENDING",
  "delivery_address": "456 New St, Anytown, AN 12345",
  "contact_phone": "+1-987-654-3210",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T10:30:00Z"
}
```

### Delete Order

Delete an existing order.

**Endpoint:** `DELETE /orders/{id}/`

**Permission:** 
- Buyer can delete their own PENDING orders
- Admin can delete any order

**Response (204 No Content)**

### My Orders (Buyer)

Get a list of orders placed by the authenticated buyer.

**Endpoint:** `GET /orders/my_orders/`

**Permission:** Authenticated users with BUYER role

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "PENDING",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T09:15:00Z"
  }
]
```

### Seller Orders

Get a list of orders related to the authenticated seller's inventory.

**Endpoint:** `GET /orders/seller_orders/` or `GET /v1/seller/orders/`

**Permission:** Authenticated users with SELLER role

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "PENDING",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T09:15:00Z"
  }
]
```

### Approve Order

Approve a pending order.

**Endpoint:** `POST /orders/{id}/approve/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "APPROVED",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T11:30:00Z"
}
```

### Reject Order

Reject a pending order.

**Endpoint:** `POST /orders/{id}/reject/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "REJECTED",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T11:30:00Z"
}
```

### Cancel Order

Cancel an order (can be done by the buyer).

**Endpoint:** `POST /orders/{id}/cancel/`

**Permission:** Buyer who placed the order

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "CANCELLED",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-20T12:00:00Z"
}
```

### Mark Order as Delivered

Mark an approved order as delivered.

**Endpoint:** `POST /orders/{id}/mark-delivered/`

**Permission:** Seller who owns the inventory or admin

**Response (200 OK):**
```json
{
  "id": 1,
  "gas_inventory": 1,
  "gas_details": {
    "brand": "JIBU",
    "weight_kg": 6.0,
    "unit_price": 2500.0,
    "location": "Nairobi"
  },
  "buyer": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "quantity": 2,
  "total_price": 5000.0,
  "status": "DELIVERED",
  "delivery_address": "123 Main St, Anytown, AN 12345",
  "contact_phone": "+1-123-456-7890",
  "created_at": "2023-06-20T09:15:00Z",
  "updated_at": "2023-06-21T14:30:00Z"
}
```

### Admin: List Pending Orders

Get a list of pending orders for admin approval.

**Endpoint:** `GET /v1/admin/orders/pending/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "gas_inventory": 2,
    "gas_details": {
      "brand": "MERU",
      "weight_kg": 13.0,
      "unit_price": 4500.0,
      "location": "Mombasa"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 1,
    "total_price": 4500.0,
    "status": "PENDING",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-21T09:15:00Z",
    "updated_at": "2023-06-21T09:15:00Z"
  }
]
```

## Invoices

### List All Invoices

Get a list of all invoices for the current user.

**Endpoint:** `GET /invoices/`

**Permission:** 
- Admin can see all invoices
- Buyers can see invoices for their orders
- Sellers can see invoices for their inventory orders

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "order": 1,
    "order_details": {
      "id": 1,
      "gas_inventory": 1,
      "gas_details": {
        "brand": "JIBU",
        "weight_kg": 6.0,
        "unit_price": 2500.0,
        "location": "Nairobi"
      },
      "buyer": 1,
      "buyer_name": "johndoe",
      "seller_name": "janesmith",
      "quantity": 2,
      "total_price": 5000.0,
      "status": "APPROVED",
      "delivery_address": "123 Main St, Anytown, AN 12345",
      "contact_phone": "+1-123-456-7890",
      "created_at": "2023-06-20T09:15:00Z",
      "updated_at": "2023-06-20T11:30:00Z"
    },
    "invoice_number": "INV-A1B2C3D4",
    "is_paid": false,
    "admin_approval": false,
    "admin_approval_date": null,
    "payment_date": null,
    "created_at": "2023-06-20T11:35:00Z"
  }
]
```

### Retrieve Invoice

Get details of a specific invoice.

**Endpoint:** `GET /invoices/{id}/`

**Permission:** 
- Admin can see any invoice
- Buyer can see invoices for their orders
- Seller can see invoices for their inventory orders

**Response (200 OK):**
```json
{
  "id": 1,
  "order": 1,
  "order_details": {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "APPROVED",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T11:30:00Z"
  },
  "invoice_number": "INV-A1B2C3D4",
  "is_paid": false,
  "admin_approval": false,
  "admin_approval_date": null,
  "payment_date": null,
  "created_at": "2023-06-20T11:35:00Z"
}
```

### Create Invoice

Create a new invoice for an order.

**Endpoint:** `POST /invoices/` or `POST /v1/seller/invoice/`

**Permission:** Authenticated seller who owns the inventory associated with the order

**Request Body:**
```json
{
  "order": 1
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "order": 1,
  "order_details": {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "APPROVED",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T11:30:00Z"
  },
  "invoice_number": "INV-A1B2C3D4",
  "is_paid": false,
  "admin_approval": false,
  "admin_approval_date": null,
  "payment_date": null,
  "created_at": "2023-06-20T11:35:00Z"
}
```

### Approve Invoice

Approve an invoice by admin.

**Endpoint:** `POST /invoices/{id}/approve/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
{
  "id": 1,
  "order": 1,
  "order_details": {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "APPROVED",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T11:30:00Z"
  },
  "invoice_number": "INV-A1B2C3D4",
  "is_paid": false,
  "admin_approval": true,
  "admin_approval_date": "2023-06-21T10:15:00Z",
  "payment_date": null,
  "created_at": "2023-06-20T11:35:00Z"
}
```

### Mark Invoice as Paid

Mark an invoice as paid.

**Endpoint:** `POST /invoices/{id}/mark-as-paid/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
{
  "id": 1,
  "order": 1,
  "order_details": {
    "id": 1,
    "gas_inventory": 1,
    "gas_details": {
      "brand": "JIBU",
      "weight_kg": 6.0,
      "unit_price": 2500.0,
      "location": "Nairobi"
    },
    "buyer": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "quantity": 2,
    "total_price": 5000.0,
    "status": "APPROVED",
    "delivery_address": "123 Main St, Anytown, AN 12345",
    "contact_phone": "+1-123-456-7890",
    "created_at": "2023-06-20T09:15:00Z",
    "updated_at": "2023-06-20T11:30:00Z"
  },
  "invoice_number": "INV-A1B2C3D4",
  "is_paid": true,
  "admin_approval": true,
  "admin_approval_date": "2023-06-21T10:15:00Z",
  "payment_date": "2023-06-22T09:30:00Z",
  "created_at": "2023-06-20T11:35:00Z"
}
```

### Admin: List Pending Invoices

Get a list of pending invoices that need admin approval.

**Endpoint:** `GET /v1/admin/invoices/pending/`

**Permission:** Authenticated users with ADMIN role

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "order": 2,
    "order_details": {
      "id": 2,
      "gas_inventory": 2,
      "gas_details": {
        "brand": "MERU",
        "weight_kg": 13.0,
        "unit_price": 4500.0,
        "location": "Mombasa"
      },
      "buyer": 1,
      "buyer_name": "johndoe",
      "seller_name": "janesmith",
      "quantity": 1,
      "total_price": 4500.0,
      "status": "APPROVED",
      "delivery_address": "123 Main St, Anytown, AN 12345",
      "contact_phone": "+1-123-456-7890",
      "created_at": "2023-06-21T09:15:00Z",
      "updated_at": "2023-06-21T10:30:00Z"
    },
    "invoice_number": "INV-E5F6G7H8",
    "is_paid": false,
    "admin_approval": false,
    "admin_approval_date": null,
    "payment_date": null,
    "created_at": "2023-06-21T10:35:00Z"
  }
]
```

## Payments

### List All Payments

Get a list of all payments for the current user.

**Endpoint:** `GET /payments/`

**Permission:** 
- Admin can see all payments
- Buyers can see payments for their orders
- Sellers can see payments for their inventory orders

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "invoice": 1,
    "invoice_details": {
      "id": 1,
      "order": 1,
      "order_details": {
        "id": 1,
        "gas_inventory": 1,
        "gas_details": {
          "brand": "JIBU",
          "weight_kg": 6.0,
          "unit_price": 2500.0,
          "location": "Nairobi"
        },
        "buyer": 1,
        "buyer_name": "johndoe",
        "seller_name": "janesmith",
        "quantity": 2,
        "total_price": 5000.0,
        "status": "APPROVED",
        "delivery_address": "123 Main St, Anytown, AN 12345",
        "contact_phone": "+1-123-456-7890",
        "created_at": "2023-06-20T09:15:00Z",
        "updated_at": "2023-06-20T11:30:00Z"
      },
      "invoice_number": "INV-A1B2C3D4",
      "is_paid": true,
      "admin_approval": true,
      "admin_approval_date": "2023-06-21T10:15:00Z",
      "payment_date": "2023-06-22T09:30:00Z",
      "created_at": "2023-06-20T11:35:00Z"
    },
    "amount": 5000.0,
    "status": "COMPLETED",
    "transaction_id": "TXN123456789",
    "payment_method": "Admin Approved",
    "created_at": "2023-06-22T09:30:00Z",
    "updated_at": "2023-06-22T09:30:00Z"
  }
]
```

### Retrieve Payment

Get details of a specific payment.

**Endpoint:** `GET /payments/{id}/`

**Permission:** 
- Admin can see any payment
- Buyer can see payments for their orders
- Seller can see payments for their inventory orders

**Response (200 OK):**
```json
{
  "id": 1,
  "invoice": 1,
  "invoice_details": {
    "id": 1,
    "order": 1,
    "order_details": {
      "id": 1,
      "gas_inventory": 1,
      "gas_details": {
        "brand": "JIBU",
        "weight_kg": 6.0,
        "unit_price": 2500.0,
        "location": "Nairobi"
      },
      "buyer": 1,
      "buyer_name": "johndoe",
      "seller_name": "janesmith",
      "quantity": 2,
      "total_price": 5000.0,
      "status": "APPROVED",
      "delivery_address": "123 Main St, Anytown, AN 12345",
      "contact_phone": "+1-123-456-7890",
      "created_at": "2023-06-20T09:15:00Z",
      "updated_at": "2023-06-20T11:30:00Z"
    },
    "invoice_number": "INV-A1B2C3D4",
    "is_paid": true,
    "admin_approval": true,
    "admin_approval_date": "2023-06-21T10:15:00Z",
    "payment_date": "2023-06-22T09:30:00Z",
    "created_at": "2023-06-20T11:35:00Z"
  },
  "amount": 5000.0,
  "status": "COMPLETED",
  "transaction_id": "TXN123456789",
  "payment_method": "Admin Approved",
  "created_at": "2023-06-22T09:30:00Z",
  "updated_at": "2023-06-22T09:30:00Z"
}
```

### Create Payment

Create a new payment for an invoice.

**Endpoint:** `POST /payments/`

**Permission:** Authenticated user with appropriate access to the invoice

**Request Body:**
```json
{
  "invoice": 1,
  "amount": 5000.0,
  "payment_method": "Mobile Money",
  "transaction_id": "TXN123456789"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "invoice": 1,
  "invoice_details": {
    "id": 1,
    "order": 1,
    "order_details": {
      "id": 1,
      "gas_inventory": 1,
      "gas_details": {
        "brand": "JIBU",
        "weight_kg": 6.0,
        "unit_price": 2500.0,
        "location": "Nairobi"
      },
      "buyer": 1,
      "buyer_name": "johndoe",
      "seller_name": "janesmith",
      "quantity": 2,
      "total_price": 5000.0,
      "status": "APPROVED",
      "delivery_address": "123 Main St, Anytown, AN 12345",
      "contact_phone": "+1-123-456-7890",
      "created_at": "2023-06-20T09:15:00Z",
      "updated_at": "2023-06-20T11:30:00Z"
    },
    "invoice_number": "INV-A1B2C3D4",
    "is_paid": false,
    "admin_approval": true,
    "admin_approval_date": "2023-06-21T10:15:00Z",
    "payment_date": null,
    "created_at": "2023-06-20T11:35:00Z"
  },
  "amount": 5000.0,
  "status": "PENDING",
  "transaction_id": "TXN123456789",
  "payment_method": "Mobile Money",
  "created_at": "2023-06-22T09:30:00Z",
  "updated_at": "2023-06-22T09:30:00Z"
}
```

### Update Payment

Update an existing payment.

**Endpoint:** `PUT /payments/{id}/` or `PATCH /payments/{id}/`

**Permission:** Admin or payment creator with appropriate permissions

**Request Body (PATCH - partial update):**
```json
{
  "status": "COMPLETED",
  "transaction_id": "TXN987654321"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "invoice": 1,
  "invoice_details": {
    "id": 1,
    "order": 1,
    "order_details": {
      "id": 1,
      "gas_inventory": 1,
      "gas_details": {
        "brand": "JIBU",
        "weight_kg": 6.0,
        "unit_price": 2500.0,
        "location": "Nairobi"
      },
      "buyer": 1,
      "buyer_name": "johndoe",
      "seller_name": "janesmith",
      "quantity": 2,
      "total_price": 5000.0,
      "status": "APPROVED",
      "delivery_address": "123 Main St, Anytown, AN 12345",
      "contact_phone": "+1-123-456-7890",
      "created_at": "2023-06-20T09:15:00Z",
      "updated_at": "2023-06-20T11:30:00Z"
    },
    "invoice_number": "INV-A1B2C3D4",
    "is_paid": false,
    "admin_approval": true,
    "admin_approval_date": "2023-06-21T10:15:00Z",
    "payment_date": null,
    "created_at": "2023-06-20T11:35:00Z"
  },
  "amount": 5000.0,
  "status": "COMPLETED",
  "transaction_id": "TXN987654321",
  "payment_method": "Mobile Money",
  "created_at": "2023-06-22T09:30:00Z",
  "updated_at": "2023-06-22T10:15:00Z"
}
```

## Ratings

### List All Ratings

Get a list of all ratings for the current user.

**Endpoint:** `GET /ratings/`

**Permission:** 
- Admin can see all ratings
- Buyers can see ratings for their orders
- Sellers can see ratings for their inventory orders

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "order": 1,
    "buyer_name": "johndoe",
    "seller_name": "janesmith",
    "rating": 5,
    "comment": "Excellent service and delivery was on time!",
    "created_at": "2023-06-23T14:00:00Z"
  }
]
```

### Retrieve Rating

Get details of a specific rating.

**Endpoint:** `GET /ratings/{id}/`

**Permission:** 
- Admin can see any rating
- Buyer can see ratings for their orders
- Seller can see ratings for their inventory orders

**Response (200 OK):**
```json
{
  "id": 1,
  "order": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "rating": 5,
  "comment": "Excellent service and delivery was on time!",
  "created_at": "2023-06-23T14:00:00Z"
}
```

### Create Rating

Create a new rating for an order.

**Endpoint:** `POST /ratings/` or `POST /v1/feedback/`

**Permission:** Buyer who placed the order

**Request Body:**
```json
{
  "order": 1,
  "rating": 5,
  "comment": "Excellent service and delivery was on time!"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "order": 1,
  "buyer_name": "johndoe",
  "seller_name": "janesmith",
  "rating": 5,
  "comment": "Excellent service and delivery was on time!",
  "created_at": "2023-06-23T14:00:00Z"
}
```

## API Versioning

The API supports two ways of accessing endpoints:

1. **Default Endpoints**: These use the standard REST pattern (e.g., `/inventory/`, `/orders/`, etc.)
2. **v1 Endpoints**: These provide backward compatibility and follow the format `/v1/...` (e.g., `/v1/gas/`, `/v1/orders/`, etc.)

Both endpoint types provide the same functionality, but may have slightly different response formats. For new development, it's recommended to use the default endpoints.
