import tables
import time
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

def main():
    """Small"""
    uninformed_time_small=[]
    tables.createDB("A3Small.db","small","uninformed")
    for i in range(50):
        time = Question2("A3Small.db")
        uninformed_time_small.append(time)
      
    selfoptimized_time_small=[]
    tables.createDB("A3Small.db","small","self-optimized")
    for i in range(50):
        time = Question2("A3Small.db")
        selfoptimized_time_small.append(time)
     
    useroptimized_time_small=[]
    tables.createDB("A3Small.db","small","user-optimized")
    for i in range(50):
        time = Question2("A3Small.db")
        useroptimized_time_small.append(time)
    
    """Medium"""
    uninformed_time_medium=[]
    tables.createDB("A3Medium.db","medium","uninformed")
    for i in range(50):
        time = Question2("A3Medium.db")
        uninformed_time_medium.append(time)
    selfoptimized_time_medium=[]
    tables.createDB("A3Medium.db","medium","self-optimized")
    for i in range(50):
        time = Question2("A3Medium.db")
        selfoptimized_time_medium.append(time)
    useroptimized_time_medium=[]
    tables.createDB("A3Medium.db","medium","user-optimized")
    for i in range(50):
        time = Question2("A3Medium.db")
        useroptimized_time_medium.append(time)
    
    """Large"""
    uninformed_time_large=[]
    tables.createDB("A3Large.db","large","uninformed")
    for i in range(50):
        time = Question2("A3Large.db")
        uninformed_time_large.append(time)
    selfoptimized_time_large=[]
    tables.createDB("A3Large.db","large","self-optimized")
    for i in range(50):
        time = Question2("A3Large.db")
        selfoptimized_time_large.append(time)
    useroptimized_time_large=[]
    tables.createDB("A3Large.db","large","user-optimized")
    for i in range(50):
        time = Question2("A3Large.db")
        useroptimized_time_large.append(time)


    categories = (
        "SmallDB\n",
        "MediumDB\n",
        "LargeDB\n",
    )
    weight_counts = {
        "Uninformed": np.array([np.mean(uninformed_time_small), np.mean(uninformed_time_medium), np.mean(uninformed_time_large)]),
        "Self-Optimized": np.array([np.mean(selfoptimized_time_small), np.mean(selfoptimized_time_medium), np.mean(selfoptimized_time_large)]),
        "User-Optimized": np.array([np.mean(useroptimized_time_small), np.mean(useroptimized_time_medium), np.mean(useroptimized_time_large)])
    }

    width = 0.5

    fig, ax = plt.subplots()
    bottom = np.zeros(3)

    for boolean, weight_count in weight_counts.items():
        p = ax.bar(categories, weight_count, width, label=boolean, bottom=bottom)
        bottom += weight_count

    ax.set_title("Average time to complete task for each optimization approach")
    ax.legend(loc="upper left")

    plt.show()
    





def Question2(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    c.execute("""
    SELECT C.customer_postal_code
    FROM Customers C
    ORDER BY RANDOM()
    LIMIT 1;
    """)
    random_postal_code = c.fetchall()
    c.execute("""
    CREATE VIEW IF NOT EXISTS OrderSize AS
        SELECT order_id AS oid, SUM(order_item_id) AS size
        FROM Order_items
        GROUP BY order_id;
    """)

    start_time = time.perf_counter()
    c.execute("""
    SELECT COUNT(DISTINCT oi.order_id)
    FROM Order_items oi
    WHERE oi.order_id IN (
        SELECT oi2.order_id
        FROM Order_items oi2
        GROUP BY oi2.order_id
        HAVING COUNT(DISTINCT oi2.order_item_id) > (select avg(size)
                                                    From OrderSize)
        )
        AND oi.order_id IN (
            SELECT o.order_id
            FROM Orders o
            WHERE o.customer_id IN (
                SELECT c.customer_id 
                FROM Customers c 
                WHERE c.customer_postal_code = ?
                )
        )
    
""", (random_postal_code[0][0],))
    
    end_time = time.perf_counter()
    elapsed_time = (end_time - start_time) * 1000
    conn.close()
    return elapsed_time

main()