# to_sqlite.py
# 作用：把 CSV 数据存入 SQLite 数据库
import pandas as pd
import sqlite3

# 1. 读取清洗后的数据
# orders = pd.read_csv("orders_joined.csv")
users = pd.read_csv("users.csv")
items = pd.read_csv("items.csv")

# 2. 连接 SQLite 数据库（如果没有这个文件，会自动创建）
conn = sqlite3.connect("campus.db")
# 先删掉旧表，防止多次运行数据重复
conn.execute("DROP TABLE IF EXISTS orders")

# 分块读取并写入
chunk_size = 100000
for chunk in pd.read_csv("orders_joined.csv", chunksize=chunk_size):
    chunk.to_sql("orders", conn, if_exists="append", index=False)

# 3. 写入数据表
# orders.to_sql("orders", conn, if_exists="replace", index=False)
users.to_sql("users", conn, if_exists="replace", index=False)
items.to_sql("items", conn, if_exists="replace", index=False)

print("数据已成功导入 SQLite 数据库！")

# 4. 验证一下，查查订单总数
result = pd.read_sql("SELECT COUNT(*) AS cnt FROM orders", conn)
print(f"数据库 orders 表里的记录数: {result['cnt'][0]} 条")

conn.close()