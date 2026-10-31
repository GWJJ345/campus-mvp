# gen_data.py
# 作用：生成模拟数据，并故意制造一些脏数据（空值）供后续清洗
import csv
import random
from datetime import datetime, timedelta

random.seed(42)  # 固定随机种子，保证每次生成的数据一样

# 1. 生成用户
users = []
campuses = ["A校区", "B校区", "C校区"]
for i in range(1, 100001):
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

# 3. 生成订单（流式写入版）
print("开始生成订单数据...")

with open("orders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["order_id", "buyer_id", "item_id", "amount", "order_time"])
    writer.writeheader()

    base_time = datetime(2024, 1, 1)
    total_orders = 100000  # 100 万行，几十秒就能跑完！
    
    for i in range(1, total_orders + 1):
        # 抽买家、商品、小时
        buyer_id = random.choices(range(1, 100001), weights=[20]*20000 + [1]*80000, k=1)[0]
        item_id = random.choices(range(1, 201), weights=[30]*10 + [1]*190, k=1)[0]
        order_hour = random.choices(range(24), weights=[1]*6 + [5]*13 + [10]*5, k=1)[0]

        order_time = base_time + timedelta(
            days=random.randint(0, 30),
            hours=order_hour,
            minutes=random.randint(0, 59),
        )
        # 顺手制造脏数据：每 20 万条里，大概有 1 条会是空值
        amount = round(random.uniform(10, 500), 2)
        if random.random() < 0.000005:  
            amount = ""

        # 生成一条，写一条
        writer.writerow({
            "order_id": i,
            "buyer_id": buyer_id,
            "item_id": item_id,
            "amount": amount,
            "order_time": order_time.strftime("%Y-%m-%d %H:%M:%S"),
        })
        
        # 进度提示
        if i % 200000 == 0:
            print(f"已生成 {i} 行...")

print(f"数据生成完毕！共生成 {total_orders} 条订单。")



