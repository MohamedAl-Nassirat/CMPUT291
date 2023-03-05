import tables
import time
import sqlite3


def main():
    """Small"""
    uninformed_time_small=[]
    tables.createDB("A3Small.db","small","uninformed")
    for i in range(50):
        time = Question1("A3Small.db")
        uninformed_time_small.append(time)
      
    selfoptimized_time_small=[]
    tables.createDB("A3Small.db","small","self-optimized")
    for i in range(50):
        time = Question1("A3Small.db")
        selfoptimized_time_small.append(time)
     
    useroptimized_time_small=[]
    tables.createDB("A3Small.db","small","user-optimized")
    for i in range(50):
        time = Question1("A3Small.db")
        useroptimized_time_small.append(time)
    
    """Medium"""
    uninformed_time_medium=[]
    tables.createDB("A3Medium.db","medium","uninformed")
    for i in range(50):
        time = Question1("A3Medium.db")
        uninformed_time_medium.append(time)
    selfoptimized_time_medium=[]
    tables.createDB("A3Medium.db","medium","self-optimized")
    for i in range(50):
        time = Question1("A3Medium.db")
        selfoptimized_time_medium.append(time)
    useroptimized_time_medium=[]
    tables.createDB("A3Medium.db","medium","user-optimized")
    for i in range(50):
        time = Question1("A3Medium.db")
        useroptimized_time_medium.append(time)
    
    
    """Large"""
    uninformed_time_large=[]
    tables.createDB("A3Large.db","large","uninformed")
    for i in range(50):
        time = Question1("A3Large.db")
        uninformed_time_large.append(time)
    selfoptimized_time_large=[]
    tables.createDB("A3Large.db","large","self-optimized")
    for i in range(50):
        time = Question1("A3Large.db")
        selfoptimized_time_large.append(time)
    useroptimized_time_large=[]
    tables.createDB("A3Large.db","large","user-optimized")
    for i in range(50):
        time = Question1("A3Large.db")
        useroptimized_time_large.append(time)
    

    # ## Write times out into txt for spreadsheet
    # file1 = open("Q1_Timing.txt", "w")
    # file1.write("useroptimized_time_large " + "selfoptimized_time_medium " + "uninformed_time_small " + "\n")
    # for i in range(len(useroptimized_time_large)):
    #     file1.write(str(uninformed_time_small[i]) + "\n")






def Question1(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    
    c.execute("""
    SELECT C.customer_postal_code
    FROM Customers C
    ORDER BY RANDOM()
    LIMIT 1;
    """)
    random_postal_code = c.fetchall()
    start_time = time.perf_counter()
    c.execute("""
    SELECT COUNT(DISTINCT oi.order_id)
FROM Order_items oi
WHERE oi.order_id IN (
    SELECT oi2.order_id
    FROM Order_items oi2
    GROUP BY oi2.order_id
    HAVING COUNT(DISTINCT oi2.order_item_id) > 1
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