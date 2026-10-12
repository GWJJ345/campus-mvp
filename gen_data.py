# gen_data.py
# 作用：生成模拟数据，并故意制造一些脏数据（空值）供后续清洗
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # 固定随机种子，保证每次生成的数据一样

# 1. 生成用户
users = []
campuses = ["A校区", "B校区", "C校区"]
for i in range(1, 101):
    users.append({
        "user_id": i,
        "name": f"user_{i}",
        "campus": random.choice(campuses),
    })

# 2. 生成商品
items = []
categories = ["教材", "电子产品", "生活用品", "运动器材"]
for i in range(1, 201):
    items.append({
        "item_id": i,
        "seller_id": random.randint(1, 100),
        "price": round(random.uniform(10, 500), 2),
        "category": random.choice(categories),
    })

# 3. 生成订单
orders = []
base_time = datetime(2024, 1, 1)
for i in range(1, 10000001):
    order_time = base_time + timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    orders.append({
        "order_id": i,
        "buyer_id": random.randint(1, 100),
        "item_id": random.randint(1, 200),
        "amount": round(random.uniform(10, 500), 2),
        "order_time": order_time.strftime("%Y-%m-%d %H:%M:%S"),
    })

# 4. 故意制造 5 条脏数据：把 amount 改成空值，为了后面演示数据清洗
for i in range(5):
    orders[random.randint(0, len(orders)-1)]["amount"] = ""

# 5. 写 CSV 文件的函数
def write_csv(filename, data, fieldnames):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# 6. 调用函数生成三个 CSV 文件
write_csv("users.csv", users, ["user_id", "name", "campus"])
write_csv("items.csv", items, ["item_id", "seller_id", "price", "category"])
write_csv("orders.csv", orders, ["order_id", "buyer_id", "item_id", "amount", "order_time"])

print(f"数据生成完毕！共生成 {len(orders)} 条订单, {len(users)} 个用户, {len(items)} 个商品。")