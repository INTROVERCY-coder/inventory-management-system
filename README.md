# Inventory Management System

## Mini Web App Project

**Student:** Nirbhaysingh A. Chauhan

**Project:** Inventory / Product Management System

**Backend:** Python Flask  
**Database:** SQLite  
**Frontend:** HTML, CSS, JavaScript  
**Frontend Tooling:** Node.js / npm

---

## Project Description

The Inventory Management System is a full-stack web application developed to manage product and stock information efficiently.

The application allows users to add, view, search, update, and delete product records. It also provides stock status information and low-stock alerts through a modern dashboard interface.

The project demonstrates CRUD operations, REST API development, database integration, frontend-backend communication, input validation, and dynamic webpage updates using the Fetch API.

---

## Features

- Add new products
- View all products
- Search products by:
  - Product ID
  - Product name
  - Category
- Update product quantity
- Update product price
- Delete products
- Prevent duplicate Product IDs
- Validate quantity and price values
- Prevent negative stock quantities
- Prevent negative prices
- Display stock status
- Low-stock alerts
- Out-of-stock detection
- Dynamic dashboard statistics
- Responsive dark-themed user interface
- SQLite database for persistent data storage
- REST API using Flask
- JSON-based frontend-backend communication
- Fetch API for updates without page reload

---

## Technology Stack

### Frontend

- HTML5
- CSS3
- JavaScript
- Fetch API

### Backend

- Python
- Flask

### Database

- SQLite

### Frontend Tooling

- Node.js
- npm
- package.json

---

## Project Structure

```text
inventory-management-system/
│
├── app.py
├── inventory.db
├── requirements.txt
├── package.json
├── README.md
├── .gitignore
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── venv/
