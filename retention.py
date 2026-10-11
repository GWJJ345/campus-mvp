# retention.py
# 作用：用 SQL 计算核心指标（GMV、UV、校区分布、趋势、TopN、留存）
import sqlite3
import pandas as pd

conn = sqlite3.connect("campus.db")

# 指标1：GMV（总交易额）
sql1 = "SELECT SUM(amount) AS gmv FROM orders"
print("1. 总 GMV:", pd.read_sql(sql1, conn)["gmv"][0])

# 指标2：UV（下单用户数）
sql2 = "SELECT COUNT(DISTINCT buyer_id) AS uv FROM orders"
print("2. 总 UV:", pd.read_sql(sql2, conn)["uv"][0])

# 指标3：各校区 GMV
sql3 = """
SELECT campus, SUM(amount) AS gmv
FROM orders
GROUP BY campus
ORDER BY gmv DESC
"""
print("\n3. 各校区 GMV:")
print(pd.read_sql(sql3, conn))

# 指标4：每日 GMV（趋势）
sql4 = """
SELECT DATE(order_time) AS order_date, SUM(amount) AS gmv
FROM orders
GROUP BY DATE(order_time)
ORDER BY order_date
"""
print("\n4. 每日 GMV 趋势（前5天）:")
print(pd.read_sql(sql4, conn).head())

# 指标5：Top 10 热门商品
sql5 = """
SELECT item_id, COUNT(*) AS order_count, SUM(amount) AS gmv
FROM orders
GROUP BY item_id
ORDER BY order_count DESC
LIMIT 10
"""
print("\n5. Top 10 热门商品:")
print(pd.read_sql(sql5, conn))

# 指标6：留存（第 1、3、7 天复购情况）
sql6 = """
WITH first_order AS (
    SELECT buyer_id, MIN(DATE(order_time)) AS first_date
    FROM orders
    GROUP BY buyer_id
),
user_orders AS (
    SELECT DISTINCT buyer_id, DATE(order_time) AS order_date
    FROM orders
)
SELECT
    f.first_date,
    CAST(JULIANDAY(o.order_date) - JULIANDAY(f.first_date) AS INTEGER) AS day_diff,
    COUNT(DISTINCT o.buyer_id) AS users
FROM first_order f
JOIN user_orders o ON f.buyer_id = o.buyer_id
WHERE CAST(JULIANDAY(o.order_date) - JULIANDAY(f.first_date) AS INTEGER) IN (1, 3, 7)
GROUP BY f.first_date, day_diff
ORDER BY f.first_date, day_diff
"""
print("\n6. 留存分析（第1/3/7天复购）:")
print(pd.read_sql(sql6, conn).head(20))

# 指标7：客单价 (AOV)
sql7 = "SELECT SUM(amount) / COUNT(DISTINCT order_id) AS aov FROM orders"
print("\n7. 客单价 (AOV):")
print(pd.read_sql(sql7, conn).iloc[0, 0])

# 指标8：复购率 (Repurchase Rate)
sql8 = """
SELECT CAST(SUM(CASE WHEN cnt >= 2 THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS repurchase_rate
FROM (
    SELECT buyer_id, COUNT(order_id) AS cnt
    FROM orders
    GROUP BY buyer_id
) t;
"""
print("\n8. 复购率:")
print(pd.read_sql(sql8, conn).iloc[0, 0])

# 指标9：下单时段偏好（按小时）
sql9 = """
SELECT strftime('%H', order_time) AS hour, COUNT(*) AS order_count
FROM orders
GROUP BY hour
ORDER BY hour;
"""
print("\n9. 下单时段偏好（按小时）:")
print(pd.read_sql(sql9, conn))

conn.close()