import pandas as pd
import numpy as np

rng=np.random.default_rng(42)
n=500

regions=["Mumbai","Pune","Delhi","Banglore","Hyderabad"]
categories = ["Electronics", "Clothing", "Furniture", "Groceries"]

products = {
    "Electronics": ["Laptop", "Mobile", "Headphones"],
    "Clothing": ["Shirt", "Jeans", "Jacket"],
    "Furniture": ["Chair", "Table", "Sofa"],
    "Groceries": ["Rice", "Oil", "Snacks"]
}
rows=[]

for i in range(n):
    category = rng.choice(categories)
    product = rng.choice(products[category])
    quantity = int(rng.integers(1, 11))
    unit_price = int(rng.integers(100, 5001))
    discount = float(rng.choice([0, 0.05, 0.10, 0.15]))
    revenue = round(quantity * unit_price * (1 - discount), 2)
    cost = round(quantity * unit_price * 0.65, 2)

    rows.append({
        "Order_ID": f"ORD{i+1:04d}",
        "Order_Date": pd.Timestamp("2025-01-01") +
                      pd.Timedelta(days=int(rng.integers(0, 365))),
        "Region": rng.choice(regions),
        "Category": category,
        "Product": product,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": round(revenue - cost, 2)
    })

df = pd.DataFrame(rows)

df.to_csv("data/sales_data.csv", index=False)

print("Sales dataset created successfully!")
print("Total Records:", len(df))
print(df.head())

print("\n--- DATASET INFORMATION ---")

print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nStatistical Summary:")
print(df.describe())


# DATA CLEANING

print("\n--- DATA CLEANING ---")

# Check duplicate records
print("Duplicate Records:", df.duplicated().sum())

# Check missing values
print("Missing Values:", df.isnull().sum().sum())

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.dropna()

# Convert date column
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Save cleaned dataset
df.to_csv("data/sales_data_cleaned.csv", index=False)

print("\nData Cleaning Completed!")
print("Cleaned Dataset Shape:", df.shape)

# BUSINESS INSIGHTS

print("\n===== BUSINESS INSIGHTS =====")

total_revenue = df["Revenue"].sum()
print("Total Revenue:", round(total_revenue, 2))

total_profit = df["Profit"].sum()
print("Total Profit:", round(total_profit, 2))

total_orders = df["Order_ID"].nunique()
print("Total Orders:", total_orders)

best_region = df.groupby("Region")["Revenue"].sum().idxmax()
print("Best Region:", best_region)

top_product = df.groupby("Product")["Quantity"].sum().idxmax()
print("Top Selling Product:", top_product)

print("\nCategory-wise Revenue:")
print(df.groupby("Category")["Revenue"].sum().sort_values(ascending=False))

print("\nRegion-wise Profit:")
print(df.groupby("Region")["Profit"].sum().sort_values(ascending=False))


import matplotlib.pyplot as plt
import seaborn as sns

# Category-wise Revenue Chart
plt.figure(figsize=(9, 5))

category_revenue = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)

sns.barplot(x=category_revenue.index, y=category_revenue.values)

plt.title("Category-wise Sales Revenue")
plt.xlabel("Category")
plt.ylabel("Revenue (₹)")
plt.xticks(rotation=20)
plt.tight_layout()

plt.savefig("reports/category_revenue.png")
plt.show()

# Region-wise Profit Chart
plt.figure(figsize=(9, 5))

region_profit = df.groupby("Region")["Profit"].sum().sort_values(ascending=False)

sns.barplot(x=region_profit.index, y=region_profit.values)

plt.title("Region-wise Profit Analysis")
plt.xlabel("Region")
plt.ylabel("Profit (₹)")
plt.tight_layout()

plt.savefig("reports/region_profit.png")
plt.show()

print("Business graphs created successfully!")