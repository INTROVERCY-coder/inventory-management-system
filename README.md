# 📦 Inventory Management System

A full-stack web application for managing products, stock quantities, pricing, categories, and inventory status.

This project was developed as a **Mini Web App Project – Aim 6: Inventory / Product Management System**, demonstrating practical implementation of full-stack web development, CRUD operations, REST APIs, database integration, validation, and dynamic frontend updates.

---

## 👨‍💻 Student

**Name:** Nirbhaysingh A. Chauhan

**Project:** Inventory / Product Management System

**Project Type:** Mini Web App Project

---

## 📋 Project Overview

The Inventory Management System provides a simple and user-friendly interface for maintaining product and stock information.

The application allows users to:

- Add new products
- View all products
- Search products
- Update product information
- Update stock quantities
- Update product prices
- Delete products
- Monitor stock levels
- Identify low-stock products
- Identify out-of-stock products

The frontend communicates with a Flask REST API using JavaScript Fetch API requests, while SQLite provides persistent data storage.

---

## 🎯 Aim

To design and develop an **Inventory / Product Management System web application** that enables users to add, search, update stock, and delete product records using HTML, CSS, JavaScript, Python Flask, and SQLite, demonstrating full-stack CRUD operations relevant to inventory tracking.

---

## 🎯 Objectives

The project implements the following objectives:

- Design a user-friendly frontend for product management.
- Store Product ID, Name, Category, Quantity, and Price.
- Develop RESTful API endpoints using Flask.
- Implement Create, Read, Update, and Delete operations.
- Use SQLite for persistent data storage.
- Connect the frontend and backend using HTTP requests.
- Exchange data using JSON.
- Use JavaScript Fetch API for asynchronous communication.
- Validate product information on the client and server side.
- Prevent duplicate Product IDs.
- Prevent negative quantity values.
- Prevent negative price values.
- Dynamically display product and search results without page reload.
- Display low-stock and out-of-stock information.
- Handle invalid and non-existent product operations.

---

## ✨ Key Features

### Product Management

- ➕ Add Product
- 👁️ View Products
- 🔍 Search Products
- ✏️ Edit Product
- 🗑️ Delete Product
- 📦 Update Stock
- 💰 Update Price

### Search

Products can be searched using:

- Product ID
- Product Name
- Category

### Inventory Status

The system identifies:

- 🟢 In Stock
- 🟠 Low Stock
- 🔴 Out of Stock

### Dashboard

The dashboard provides inventory statistics such as:

- Total Products
- Total Stock Quantity
- Low Stock Products
- Out of Stock Products

### Validation

The application validates:

- Required product fields
- Unique Product IDs
- Non-negative quantities
- Non-negative prices
- Valid product operations

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | HTML5 |
| Styling | CSS3 |
| Client-side Logic | JavaScript |
| Frontend Tooling | Node.js / npm |
| Backend | Python |
| Web Framework | Flask |
| Database | SQLite |
| Data Format | JSON |
| Communication | REST API / HTTP |
| API Requests | Fetch API |

---

## 🏗️ Application Architecture

```text
┌─────────────────────────────┐
│        User / Browser       │
└──────────────┬──────────────┘
               │
               │ HTML / CSS / JavaScript
               │ Fetch API
               ▼
┌─────────────────────────────┐
│       Flask REST API        │
│                             │
│  GET  POST  PUT  DELETE     │
└──────────────┬──────────────┘
               │
               │ SQL Queries
               ▼
┌─────────────────────────────┐
│          SQLite             │
│      Product Database       │
└─────────────────────────────┘
