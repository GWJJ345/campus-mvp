# analyze.py
# 作用：清洗数据（去空值、去重） + 关联（merge）用户和商品信息
import pandas as pd

# 1. 读取数据

chunk_size = 100000
cleaned_chunks = []

print("开始分块读取...")
for i, chunk in enumerate(pd.read_csv("orders.csv", chunksize=chunk_size)):
    chunk["amount"] = pd.to_numeric(chunk["amount"], errors="coerce")
    chunk = chunk.dropna(subset=["amount"])
    cleaned_chunks.append(chunk)
    print(f"已处理 {(i+1)*chunk_size} 行...")

orders = pd.concat(cleaned_chunks, ignore_index=True)

print(f"原始订单数: {len(orders)} 条")


# 4. 清洗：按 order_id 去重
orders = orders.drop_duplicates(subset=["order_id"])
# 读取维度表（就是这两行漏了）
users = pd.read_csv("users.csv")
items = pd.read_csv("items.csv")

# 然后再执行原来的关联
orders = orders.merge(users, left_on="buyer_id", right_on="user_id", how="left")
orders = orders.merge(items, on="item_id", how="left", suffixes=("", "_item"))
# 5. 关联：把用户表合并进来（获取买家所在校区）
orders = orders.merge(users, left_on="buyer_id", right_on="user_id", how="left")

# 6. 关联：把商品表合并进来（获取商品分类）
orders = orders.merge(items, on="item_id", how="left", suffixes=("", "_item"))

# 7. 保存清洗关联后的数据
orders.to_csv("orders_joined.csv", index=False)
print(f"清洗关联后订单数: {len(orders)} 条，已保存到 orders_joined.csv")
print(orders.head()) # 打印前五行看看长什么样