# 校园二手交易数据分析 MVP

## 📖 项目简介
本项目是一个基于 Python + Pandas + SQLite 搭建的**离线数据开发最小化项目**。
完整覆盖了从“模拟数据生成 -> 数据清洗与关联 -> 数据入库 -> SQL指标计算”的全流程。

## 🛠️ 技术栈
- **语言**：Python 3.x, SQL (SQLite)
- **核心库**：Pandas
- **开发工具**：VS Code, Git

## 🏗️ 数据流架构
```
[Python 生成模拟数据]  (gen_data.py)
        ↓
  users.csv / items.csv / orders.csv  (原始数据层)
        ↓
[Pandas 清洗与关联]  (analyze.py)
  - 剔除 amount 空值
  - 关联用户、商品表
        ↓
  orders_joined.csv  (清洗关联层)
        ↓
[SQLite 数据库写入]  (to_sqlite.py)
        ↓
  campus.db  (数据存储层)
        ↓
[SQL 指标计算]  (retention.py)
  - 聚合 (GROUP BY)
  - 窗口函数 / CTE
        ↓
  [终端输出最终指标]  (GMV, UV, 留存率, 客单价...)
  ```

## 📊 核心业务指标
本项目实现了以下 9 个核心数据指标：

1. **GMV（商品交易总额）**：`SUM(amount)`
2. **UV（下单用户数）**：`COUNT(DISTINCT buyer_id)`
3. **各校区 GMV 分布**
4. **每日 GMV 趋势**
5. **Top 10 热门商品**（按订单量排序）
6. **留存率**：基于 SQL CTE 和 `JULIANDAY` 计算第1/3/7天复购率
7. **客单价 (AOV)**：`SUM(amount) / COUNT(DISTINCT order_id)`
8. **复购率**：基于子查询计算下单 2 次及以上的用户占比
9. **下单时段偏好**：利用 `strftime` 提取小时，统计各时段订单分布

## 🚀 快速开始
克隆仓库：

bash
git clone https://github.com/GWJJ345/campus-mvp.git
cd campus-mvp
安装依赖：

bash
pip install pandas
按顺序运行脚本：

bash
python gen_data.py      # 生成1万条模拟数据
python analyze.py       # 清洗并关联数据
python to_sqlite.py     # 存入SQLite数据库
python retention.py     # 输出核心指标结果


## 🕳️ 踩坑记录（实战经验）
在这个项目中，我遇到并解决了以下问题：
1. **环境报错：安装 pandas 时报 Fatal error in launcher，通过使用 python -m pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple 绕过坏掉的 pip 启动器。

2. **乱码问题：Windows 终端输出中文显示 ?????，通过在终端执行 chcp 65001 切换到 UTF-8 编码解决。

3. **PowerShell 执行策略：直接运行 .\gen_data.py 报安全错，改为 python gen_data.py 明确指定解释器解决。

4. **数据清洗：原始订单中有 5 条 amount 为空的脏数据，在 analyze.py 中使用 dropna() 和 pd.to_numeric() 清洗后，订单数从 10000 条变为 9995 条。
5. **数据失真反思**：由于 `gen_data.py` 采用完全均匀的随机分布生成数据，导致复购率接近 100%、各时段订单量完全平坦，不符合真实电商场景（如二八法则、夜间低谷）。这是目前数据模拟层的缺陷，已记录在后续迭代计划中。

## 🔜 后续迭代计划 (Roadmap)

> 注：以下为项目的大致演进方向，会随着实际调研和学习进度随时调整，不构成版本承诺。

- [x] **单机全链路跑通**：完成 1 万行数据的闭环，实现 9 个核心业务指标。
- [ ] **单机性能测试**：尝试扩大数据量至 100 万行，观察内存消耗，学习使用 `chunksize` 分块读取，并评估引入 DuckDB / Polars。
- [ ] **工程化与自动化**：引入 Docker 隔离环境，并尝试加入简单的调度。
- [ ] **分布式探索**：在熟练掌握单机极限后，尝试在 WSL2/Docker 中使用 Hive / Spark SQL 重写现有逻辑。
## 👤 作者
- GitHub: @GWJJ345
- 邮箱: 2777167505@qq.com