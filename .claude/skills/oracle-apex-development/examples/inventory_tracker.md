# Inventory Management Application

## Overview
Track products, stock levels, purchase orders, and suppliers with alerts for low stock.

## Database Schema
```sql
-- Products
CREATE TABLE products (
    product_id NUMBER PRIMARY KEY,
    product_name VARCHAR2(100) NOT NULL,
    sku VARCHAR2(50) UNIQUE NOT NULL,
    category VARCHAR2(50),
    unit_price NUMBER(10,2) NOT NULL,
    reorder_level NUMBER DEFAULT 10,
    current_stock NUMBER DEFAULT 0
);

-- Suppliers
CREATE TABLE suppliers (
    supplier_id NUMBER PRIMARY KEY,
    supplier_name VARCHAR2(100) NOT NULL,
    contact_name VARCHAR2(100),
    phone VARCHAR2(20),
    email VARCHAR2(100)
);

-- Purchase Orders
CREATE TABLE purchase_orders (
    po_id NUMBER PRIMARY KEY,
    supplier_id NUMBER NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR2(20) DEFAULT 'PENDING',
    total_amount NUMBER(12,2),
    CONSTRAINT po_supplier_fk FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

-- Purchase Order Items
CREATE TABLE po_items (
    po_item_id NUMBER PRIMARY KEY,
    po_id NUMBER NOT NULL,
    product_id NUMBER NOT NULL,
    quantity NUMBER NOT NULL,
    unit_price NUMBER(10,2) NOT NULL,
    CONSTRAINT poi_po_fk FOREIGN KEY (po_id) REFERENCES purchase_orders(po_id),
    CONSTRAINT poi_product_fk FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

## Application Structure

### Page 1: Dashboard
- Low Stock Alerts (products below reorder_level)
- Pending Purchase Orders count
- Total Inventory Value
- Stock Status Chart

### Page 10: Products (Interactive Grid)
```sql
SELECT product_id, product_name, sku, category, unit_price, 
       current_stock, reorder_level,
       CASE 
           WHEN current_stock <= reorder_level THEN 'LOW STOCK'
           ELSE 'OK'
       END AS stock_status
FROM products
-- Conditional formatting: Highlight low stock in red
```

### Page 20: Product Form
- Product details
- Current stock (display only)
- Reorder level setting
- Category LOV

### Page 30: Purchase Orders (Interactive Report)
```sql
SELECT po_id, supplier_name, order_date, status, 
       TO_CHAR(total_amount, '$999,999,990.00') AS total
FROM purchase_orders p
JOIN suppliers s ON p.supplier_id = s.supplier_id
ORDER BY order_date DESC
```

### Page 40: Purchase Order Form (Master-Detail)
- PO Header: supplier, order_date, status
- PO Items: Interactive Grid (product, quantity, unit_price)
- Calculated total

### Page 50: Suppliers (Interactive Report)
- Supplier list with contact information
- Link to supplier form

## Features
- Product catalog management
- Stock level tracking
- Purchase order creation
- Low stock alerts (automatic notifications)
- Supplier management
- Inventory value reports
- Stock movement history
- Barcode scanning (mobile)

## Automation
- Low Stock Email Notification (daily job)
- Automatic stock updates when PO is received
- Reorder suggestions based on historical data
