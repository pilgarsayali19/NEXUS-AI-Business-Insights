import sqlite3
import pandas as pd

conn = sqlite3.connect("data/sales.db")

# 1. Total Revenue
print("\nTOTAL REVENUE")
print(pd.read_sql("""
SELECT SUM(Revenue) AS Total_Revenue
FROM sales
""", conn))

# 2. Total Profit
print("\nTOTAL PROFIT")
print(pd.read_sql("""
SELECT SUM(Profit) AS Total_Profit
FROM sales
""", conn))

# 3. Region-wise Sales
print("\nREGION-WISE SALES")
print(pd.read_sql("""
SELECT Region, SUM(Revenue) AS Total_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Sales DESC
""", conn))

# 4. Category-wise Revenue
print("\nCATEGORY-WISE REVENUE")
print(pd.read_sql("""
SELECT Category, SUM(Revenue) AS Total_Revenue
FROM sales
GROUP BY Category
ORDER BY Total_Revenue DESC
""", conn))

# 5. Top Selling Product
print("\nTOP SELLING PRODUCT")
print(pd.read_sql("""
SELECT Product, SUM(Quantity) AS Total_Quantity
FROM sales
GROUP BY Product
ORDER BY Total_Quantity DESC
LIMIT 1
""", conn))

conn.close()