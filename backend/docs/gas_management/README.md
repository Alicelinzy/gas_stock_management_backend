# Gas Stock Management API Documentation

## Introduction

This folder contains comprehensive documentation for the Gas Stock Management backend API. The API allows for management of gas inventory, orders, invoices, payments, and user ratings in a gas stock management system.

## Contents

- [index.md](./index.md): Overview of the API and documentation structure
- [api_documentation.md](./api_documentation.md): Detailed API endpoint documentation

## Using the Documentation

1. Start with the [index.md](./index.md) file for an overview of the API features
2. For detailed endpoint information, refer to [api_documentation.md](./api_documentation.md)

## API Features

- User authentication with JWT tokens
- Role-based access control (BUYER, SELLER, ADMIN)
- Gas inventory management
- Order processing with approval workflow
- Invoice generation and payment tracking
- User ratings and feedback

## Versioning

The API supports both default endpoints (`/inventory/`, `/orders/`, etc.) and versioned v1 endpoints (`/v1/gas/`, `/v1/orders/`, etc.) for backward compatibility.

## Getting Started

To get started with the API:

1. Register a user account with the desired role
2. Authenticate to receive a JWT token
3. Include the token in subsequent API requests

## API Structure

The API is organized into the following main sections:

1. Authentication endpoints
2. User Profile endpoints
3. Gas Inventory endpoints
4. Order endpoints
5. Invoice endpoints
6. Payment endpoints
7. Rating endpoints
