# analyze.py
# 作用：清洗数据（去空值、去重） + 关联（merge）用户和商品信息
import pandas as pd

# 1. 读取数据
orders = pd.read_csv("orders.csv")
users = pd.read_csv("users.csv")
items = pd.read_csv("items.csv")

print(f"原始订单数: {len(orders)} 条")

# 2. 清洗：把 amount 转成数字，空值自动变成 NaN
orders["amount"] = pd.to_numeric(orders["amount"], errors="coerce")

# 3. 清洗：删掉 amount 为空的行
orders = orders.dropna(subset=["amount"])
print(f"去掉空值后订单数: {len(orders)} 条")

# 4. 清洗：按 order_id 去重
orders = orders.drop_duplicates(subset=["order_id"])

# 5. 关联：把用户表合并进来（获取买家所在校区）
orders = orders.merge(users, left_on="buyer_id", right_on="user_id", how="left")

# 6. 关联：把商品表合并进来（获取商品分类）
orders = orders.merge(items, on="item_id", how="left", suffixes=("", "_item"))

# 7. 保存清洗关联后的数据
orders.to_csv("orders_joined.csv", index=False)
print(f"清洗关联后订单数: {len(orders)} 条，已保存到 orders_joined.csv")
print(orders.head()) # 打印前五行看看长什么样