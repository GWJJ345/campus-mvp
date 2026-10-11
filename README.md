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

## 📊 核心业务指标
GMV（商品交易总额）：SUM(amount)
```

UV（下单用户数）：COUNT(DISTINCT buyer_id)

各校区 GMV 分布

每日 GMV 趋势

Top 10 热门商品（按订单量排序）

留存率：基于 SQL CTE 和 JULIANDAY 计算第1/3/7天复购率

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

环境报错：安装 pandas 时报 Fatal error in launcher，通过使用 python -m pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple 绕过坏掉的 pip 启动器。

乱码问题：Windows 终端输出中文显示 ?????，通过在终端执行 chcp 65001 切换到 UTF-8 编码解决。

PowerShell 执行策略：直接运行 .\gen_data.py 报安全错，改为 python gen_data.py 明确指定解释器解决。

数据清洗：原始订单中有 5 条 amount 为空的脏数据，在 analyze.py 中使用 dropna() 和 pd.to_numeric() 清洗后，订单数从 10000 条变为 9995 条。
## 🔜 后续迭代计划
□ 将数据量扩大至 100 万行，测试单机 Pandas 极限。
□ 引入 DuckDB / Polars 替代 Pandas 进行加速。
□ 增加“复购率”、“客单价”等业务指标。
□ 尝试用 Docker 隔离运行环境。
## 👤 作者
- GitHub: @GWJJ345
- 邮箱: 2777167505@qq.com