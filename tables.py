# Uninformed
# Self-Optimized
# User-Optimized

import sqlite3
import csv
import random


def main():
    createSmallDB()

def insertRandomCustomer(filename, size):

    with open(filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            for row in csv_reader:
                rows.append({'customer_id': row['customer_id'], 'customer_postal_code': row['customer_zip_code_prefix']})
            random.shuffle(rows)
            rows = rows[:size]

        
    return rows

def insertRandomSeller(filename, size):
    with open(filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            for row in csv_reader:
                rows.append({'seller_id': row['seller_id'], 'seller_postal_code': row['seller_zip_code_prefix']})
            random.shuffle(rows)
            rows = rows[:size]
    return rows

def insertRandomOrder(filename, size):
        with open(filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            for row in csv_reader:
                rows.append({'order_id': row['order_id'], 'customer_id': row['customer_id']})
            random.shuffle(rows)
            rows = rows[:size]


def insertRandomOrderItem(filename, size):
    with open(filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            for row in csv_reader:
                rows.append({'order_id': row['order_id'], 'order_item_id': row['order_item_id'], 'product_id': row['product_id'], 'seller_id': row['seller_id']})
            random.shuffle(rows)
            rows = rows[:size]
    return rows



def createSmallDB():
    conn = sqlite3.connect("A3Small.db")
    c = conn.cursor()

    customerData = insertRandomCustomer("olist_customers_dataset.csv", 10000)
    column_names = list(customerData[0].keys())

    c.execute(""" 
    CREATE TABLE "Customers" (
    "customer_id" TEXT, 
    "customer_postal_code" INTEGER,
    PRIMARY KEY("customer_id")
    );
    """
    )
    c.execute(""" 
    CREATE TABLE Sellers (
    "seller_id" TEXT,
    "seller_postal_code" INTEGER,
    PRIMARY KEY("seller_id")
    )
    """
    )
    c.execute(""" 
    CREATE TABLE Orders (
    "order_id" TEXT,
    "customer_id" TEXT, 
    PRIMARY KEY("order_id"),
    FOREIGN KEY("customer_id") REFERENCES "Customers"("customer_id")
    )
    """
    )
    c.execute(""" 
    CREATE TABLE Order_items (
    "order_id" TEXT,
    "order_item_id" INTEGER, 
    "product_id" TEXT,
    "seller_id" TEXT,
    PRIMARY KEY("order_id","order_item_id","product_id","seller_id"),
    FOREIGN KEY("seller_id") REFERENCES "Sellers"("seller_id")
    FOREIGN KEY("order_id") REFERENCES "Orders"("order_id")
    )
    """
    )
    placeholders = ', '.join(['?' for _ in column_names])
    insert_query = f'INSERT INTO Customers ({", ".join(column_names)}) VALUES ({placeholders})'
    c.executemany(insert_query, [tuple(row[column_name] for column_name in column_names) for row in customerData])





    

    conn.commit()
    conn.close()









main()


