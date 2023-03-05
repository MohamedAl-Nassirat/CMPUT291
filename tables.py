# Uninformed
# Self-Optimized
# User-Optimized

import sqlite3
import csv
import random


def main():
    createDB("A3Small.db", "small", "uninformed")
    


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
    return rows


def insertRandomOrderItem(filename, size):
    with open(filename, 'r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            rows = []
            for row in csv_reader:
                rows.append({'order_id': row['order_id'], 'order_item_id': row['order_item_id'], 'product_id': row['product_id'], 'seller_id': row['seller_id']})
            random.shuffle(rows)
            rows = rows[:size]
    return rows



def createDB(dbName, size, mode):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()

    if mode == "uninformed":
        conn.execute('PRAGMA automatic_index = off')
        
        c.execute(""" 
        CREATE TABLE "Customers" (
        "customer_id" TEXT, 
        "customer_postal_code" INTEGER
        );
        """
        )
        c.execute(""" 
        CREATE TABLE Sellers (
        "seller_id" TEXT,
        "seller_postal_code" INTEGER
        )
        """
        )
        c.execute(""" 
        CREATE TABLE Orders (
        "order_id" TEXT,
        "customer_id" TEXT
        )
        """
        )
        c.execute(""" 
        CREATE TABLE Order_items (
        "order_id" TEXT,
        "order_item_id" INTEGER, 
        "product_id" TEXT,
        "seller_id" TEXT
        )
        """
        )


    if size  == "small":
        customerData = insertRandomCustomer("olist_customers_dataset.csv", 10000)
        column_customer = list(customerData[0].keys())

        sellerData = insertRandomSeller("olist_sellers_dataset.csv", 500)
        column_seller = list(sellerData[0].keys())

        orderData = insertRandomOrder("olist_orders_dataset.csv", 10000)
        column_order = list(orderData[0].keys())

        orderItemsData = insertRandomOrderItem("olist_order_items_dataset.csv", 2000)
        column_orderItem = list(orderItemsData[0].keys())

    elif size == "medium":
        customerData = insertRandomCustomer("olist_customers_dataset.csv", 20000)
        column_customer = list(customerData[0].keys())

        sellerData = insertRandomSeller("olist_sellers_dataset.csv", 750)
        column_seller = list(sellerData[0].keys())

        orderData = insertRandomOrder("olist_orders_dataset.csv", 20000)
        column_order = list(orderData[0].keys())

        orderItemsData = insertRandomOrderItem("olist_order_items_dataset.csv", 4000)
        column_orderItem = list(orderItemsData[0].keys())
        
    elif size == "large":
        customerData = insertRandomCustomer("olist_customers_dataset.csv", 33000)
        column_customer = list(customerData[0].keys())

        sellerData = insertRandomSeller("olist_sellers_dataset.csv", 1000)
        column_seller = list(sellerData[0].keys())

        orderData = insertRandomOrder("olist_orders_dataset.csv", 33000)
        column_order = list(orderData[0].keys())

        orderItemsData = insertRandomOrderItem("olist_order_items_dataset.csv", 10000)
        column_orderItem = list(orderItemsData[0].keys())





   
    placeholders = ', '.join(['?' for _ in column_customer])
    insert_query = f'INSERT INTO Customers ({", ".join(column_customer)}) VALUES ({placeholders})'
    c.executemany(insert_query, [tuple(row[column_name] for column_name in column_customer) for row in customerData])

    placeholders2 = ', '.join(['?' for _ in column_seller])
    insert_query = f'INSERT INTO Sellers ({", ".join(column_seller)}) VALUES ({placeholders2})'
    c.executemany(insert_query, [tuple(row[column_seller] for column_seller in column_seller) for row in sellerData])

    placeholders3 = ', '.join(['?' for _ in column_order])
    insert_query = f'INSERT INTO Orders ({", ".join(column_order)}) VALUES ({placeholders3})'
    c.executemany(insert_query, [tuple(row[column_order] for column_order in column_order) for row in orderData])

    placeholders4 = ', '.join(['?' for _ in column_orderItem])
    insert_query = f'INSERT INTO Order_items ({", ".join(column_orderItem)}) VALUES ({placeholders4})'
    c.executemany(insert_query, [tuple(row[column_orderItem] for column_orderItem in column_orderItem) for row in orderItemsData])





    

    conn.commit()
    conn.close()









main()


