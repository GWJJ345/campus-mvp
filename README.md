# 校园二手交易数据分析 MVP

## 📖 项目简介
本项目是一个基于 Python + Pandas + SQLite 搭建的**离线数据开发最小化项目**。
完整覆盖了从“模拟数据生成 -> 数据清洗与关联 -> 数据入库 -> SQL指标计算”的全流程。

### 💡 核心技术亮点
- **流式写入规避 OOM**：摒弃全量列表加载，采用微批处理与流式写入（`writer.writerow`），将千万级数据生成的内存占用降至 MB 级别，彻底解决单机内存溢出假死问题。
- **真实业务分布模拟**：基于二八定律与人类作息，使用 `random.choices` 引入权重机制，完美模拟电商“爆款商品”与“晚间下单高峰”。
- **分块读取技术**：在清洗阶段引入 `chunksize` 分块读取，保障大数据量下的读取稳定性。

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

## 📊 核心业务指标验证（基于 100 万行测试数据）

本项目实现了以下 9 个核心数据指标，并跑出了贴近真实业务的数据结果：
1. **总 GMV**：25,502,542.26 元 （*把这里换成你最新跑出来的 GMV*）
2. **总 UV（下单用户数）**：34,548 人 （*换成你的 UV*）
3. **各校区 GMV 分布**：B校区 > C校区 > A校区 （*看你的最新排名*）
4. **每日 GMV 趋势**：日均约 83 万
5. **Top 10 热门商品**：受权重影响，头部商品销量呈断层式领先
6. **留存率**：基于 SQL CTE 和 `JULIANDAY` 计算第1/3/7天复购率
7. **客单价 (AOV)**：255.02 元
8. **复购率**：**57.6%** （*换成你最新的复购率*）
9. **下单时段偏好**：呈现明显的作息规律（凌晨低谷，晚间 19:00-23:00 为波峰）

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
5. **OOM 假死排查与重构**：最初使用 `List.append()` 全量生成 1000 万行数据，导致系统虚拟内存爆满（Swap），CPU 占用率跌至 1% 且程序假死。经排查后重构为**“流式写入”**方案，实现边生成边落盘，内存平稳。
6. **数据分布失真反思**：最初采用绝对均匀随机分布，导致复购率高达 100%、时段订单量呈直线。后引入 `random.choices` 权重参数，重构数据生成器，使指标具备真实业务分析价值。

🔜 后续迭代计划 (Roadmap)

注：以下为项目的大致演进方向，会随着实际调研和学习进度随时调整。

☑ v0.1 单机全链路跑通：完成 1 万行数据的闭环，实现 9 个核心业务指标。
☑ v1.0 单机性能测试：扩大数据量至 100 万行，学习使用 chunksize 解决读取 OOM。
☑ v1.2 流式写入与真实分布：重构 gen_data.py，引入流式写入解决生成 OOM；加入权重分布模拟真实电商业务。
□ v2.0 工程化与自动化：引入 Docker 隔离环境，并尝试加入简单的调度。
□ v3.0 分布式探索：尝试在 WSL2 / Docker 中使用 Hive / Spark SQL 重写现有逻辑。

## 👤 作者
- GitHub: @GWJJ345
- 邮箱: 2777167505@qq.com