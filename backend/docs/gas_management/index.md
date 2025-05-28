# Gas Stock Management API Documentation

Welcome to the Gas Stock Management API documentation. This documentation provides comprehensive information about the API endpoints, request/response formats, and authentication requirements.

## Available Documentation

- [API Documentation](./api_documentation.md) - Detailed documentation for all API endpoints

## Overview

The Gas Stock Management API allows users to:

1. **User Management**
   - Register users with different roles (BUYER, SELLER, ADMIN)
   - Authenticate using JWT tokens

2. **Inventory Management**
   - Create, update, and delete gas inventory items
   - Filter and search inventory by multiple criteria

3. **Order Management**
   - Place orders for gas inventory items
   - Track order status through the full lifecycle
   - Approve, reject, or cancel orders

4. **Invoicing and Payments**
   - Generate invoices for approved orders
   - Process payments for invoices
   - Track payment status

5. **Feedback and Ratings**
   - Submit ratings and feedback for completed orders
   - View ratings for sellers

## API Versioning

The API supports two ways of accessing endpoints:

1. **Default Endpoints**: These use the standard REST pattern (e.g., `/inventory/`, `/orders/`, etc.)
2. **v1 Endpoints**: These provide backward compatibility and follow the format `/v1/...` (e.g., `/v1/gas/`, `/v1/orders/`, etc.)

Both endpoint types provide the same functionality, but may have slightly different response formats. For new development, it's recommended to use the default endpoints.

## Authentication

Authentication is managed using JWT (JSON Web Tokens). Include the token in the Authorization header for all authenticated requests:

```
Authorization: Bearer <your_token_here>
```

## User Roles

The system has three user roles:

1. **BUYER**: Can browse inventory, place orders, and leave ratings
2. **SELLER**: Can manage inventory and view orders for their inventory
3. **ADMIN**: Has full access to the system, including approving orders and invoices
