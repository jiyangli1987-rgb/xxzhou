# Python 操作 SQLite 完整教程（按安装→增删改查顺序）

SQLite 核心优势是 **无需单独安装数据库服务**，且 Python 自带操作接口，全程零额外配置，跟着步骤走即可上手！

## 一、安装数据库（无需额外操作！）

SQLite 是 **嵌入式数据库**，无需像 MySQL 那样下载安装服务端：

- 它的数据存储在单个 `.db` 文件中，创建数据库时自动生成该文件；
- 支持 Windows、Mac、Linux 全平台，无需配置环境变量。

简单说：**跳过 “安装数据库” 步骤**，直接进入下一步！

## 二、安装依赖（Python 自带，无需额外安装！）

Python 标准库内置 `sqlite3` 模块（对 SQLite C 引擎的封装），无需用 `pip` 安装任何依赖：

- 支持 Python 2.7+、3.3+ 所有版本；
- 验证是否可用：打开终端 / 命令行，输入 `python` 进入交互模式，执行以下代码无报错即正常：
    
    python
    
    运行
    
    ```python
    import sqlite3  # 无报错则说明依赖已就绪
    ```
    

## 三、核心操作：从创建表到增删改查

以下所有操作均基于 Python 交互式环境或 `.py` 脚本，全程使用单文件数据库（`test.db`）演示。

### 第一步：连接数据库 + 创建表

连接数据库时，若指定的 `.db` 文件不存在，SQLite 会自动创建该文件；若已存在，则直接连接。

python

运行

```python
import sqlite3

# 1. 连接数据库（不存在则自动创建 test.db 文件）
# connect() 返回连接对象，是操作数据库的核心入口
conn = sqlite3.connect('test.db')

# 2. 创建游标对象（用于执行 SQL 语句）
cursor = conn.cursor()

# 3. 执行 SQL：创建用户表（user_id 主键自增，username 唯一，age 非空）
create_table_sql = """
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    email TEXT
);
"""
cursor.execute(create_table_sql)

# 4. 提交事务（创建表、增删改操作需提交才生效）
conn.commit()

# 5. 关闭游标和连接（避免资源泄露）
cursor.close()
conn.close()
```

- 关键说明：`IF NOT EXISTS` 确保表不存在时才创建，避免重复执行报错；
- 执行后，当前目录会出现 `test.db` 文件，即数据库文件。

### 第二步：数据增加（INSERT）

支持 **单条插入** 和 **批量插入**，插入后必须 `commit()` 提交事务。

python

运行

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 方式1：单条数据插入（使用 ? 占位符，避免 SQL 注入，推荐！）
user1 = ('张三', 25, 'zhangsan@test.com')
insert_sql = "INSERT INTO user (username, age, email) VALUES (?, ?, ?);"
cursor.execute(insert_sql, user1)

# 方式2：批量数据插入（executemany 效率更高）
users = [
    ('李四', 28, 'lisi@test.com'),
    ('王五', 22, None),  # 允许 email 为 NULL（表定义时未加 NOT NULL）
    ('赵六', 30, 'zhaoliu@test.com')
]
cursor.executemany(insert_sql, users)

# 提交事务（插入操作必须提交！）
conn.commit()

# 查看插入的最后一条数据的主键 ID（可选）
print("最后插入的用户 ID：", cursor.lastrowid)  # 输出：4（因为批量插入了3条，加上第一条共4条）

# 关闭资源
cursor.close()
conn.close()
```

- 注意：SQLite 中用 `?` 作为占位符（其他数据库可能用 `%s` 或 `:name`），切勿直接拼接字符串（如 `f"INSERT INTO ... {username}"`），会有 SQL 注入风险。

### 第三步：数据查看（SELECT）

支持 **查询单条**、**查询多条**、**条件查询**，查询结果通过游标获取。

python

运行

```python
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 1. 查询所有用户（fetchall() 获取所有结果）
cursor.execute("SELECT * FROM user;")
all_users = cursor.fetchall()
print("所有用户：")
for user in all_users:
    print(user)  # 输出格式：(user_id, username, age, email)，如 (1, '张三', 25, 'zhangsan@test.com')

# 2. 查询单条数据（fetchone() 获取第一条结果）
cursor.execute("SELECT username, age FROM user WHERE user_id = ?;", (1,))  # 条件查询，? 传参需用元组（即使只有1个参数）
single_user = cursor.fetchone()
print("\nID=1 的用户：", single_user)  # 输出：('张三', 25)

# 3. 条件查询（年龄 > 25 的用户）
cursor.execute("SELECT username, email FROM user WHERE age > ?;", (25,))
filtered_users = cursor.fetchall()
print("\n年龄>25 的用户：")
for user in filtered_users:
    print(user)

# 4. 限制查询结果（前2条）
cursor.execute("SELECT * FROM user LIMIT 2;")
limit_users = cursor.fetchall()
print("\n前2条用户：", limit_users)

# 关闭资源（查询操作无需 commit）
cursor.close()
conn.close()
```

- 关键方法：
    - `fetchone()`：获取下一条结果（返回元组，无结果返回 `None`）；
    - `fetchall()`：获取所有剩余结果（返回列表，无结果返回空列表）；
    - `fetchmany(n)`：获取前 n 条结果（返回列表）。

### 第四步：数据修改（UPDATE）

修改指定条件的数据，同样需要 `commit()` 提交。

python

运行

```python
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 修改用户：将 user_id=2 的用户年龄改为 29，邮箱更新
update_sql = "UPDATE user SET age = ?, email = ? WHERE user_id = ?;"
cursor.execute(update_sql, (29, 'lisi_updated@test.com', 2))

# 提交事务
conn.commit()

# 验证修改结果
cursor.execute("SELECT * FROM user WHERE user_id = 2;")
print("修改后的用户：", cursor.fetchone())

cursor.close()
conn.close()
```

- 注意：`WHERE` 条件必须加！否则会修改表中 **所有数据**（慎用）。

### 第五步：数据删除（DELETE）

删除指定条件的数据，需 `commit()` 提交。

python

运行

```python
import sqlite3

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

# 删除用户：删除 user_id=4 的用户
delete_sql = "DELETE FROM user WHERE user_id = ?;"
cursor.execute(delete_sql, (4,))

# 提交事务
conn.commit()

# 验证删除结果（查询所有用户，确认 ID=4 已消失）
cursor.execute("SELECT * FROM user;")
print("删除后的所有用户：")
for user in cursor.fetchall():
    print(user)

cursor.close()
conn.close()
```

- 警告：同样必须加 `WHERE` 条件！否则会删除表中所有数据（不可逆）。

## 四、关键注意事项

1. **事务管理**：
    
    - 增、删、改操作必须调用 `conn.commit()` 才生效；
    - 若操作出错，可调用 `conn.rollback()` 回滚事务（避免数据错乱），示例：
        
        python
        
        运行
        
        ```python
        try:
            cursor.execute(insert_sql, user1)
            conn.commit()  # 成功则提交
        except Exception as e:
            conn.rollback()  # 失败则回滚
            print("操作失败：", e)
        ```
        
2. **占位符使用**：
    
    - 必须用 `?` 作为占位符，不能直接拼接字符串（防止 SQL 注入）；
    - 传参时必须用元组（即使只有 1 个参数，如 `(1,)` 而非 `(1)` 或 `1`）。
3. **资源释放**：
    
    - 每次操作后需关闭 `cursor` 和 `conn`（或用 `with` 语句自动关闭，更简洁）：
        
        python
        
        运行
        
        ```python
        # 简化写法：with 语句自动关闭连接和游标
        with sqlite3.connect('test.db') as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM user;")
                print(cursor.fetchall())
        ```
        
4. **数据类型**：
    
    - SQLite 是弱类型数据库，无需严格匹配表定义类型（但建议按定义传入，如 `age` 传整数）；
    - 支持常见类型：`INTEGER`（整数）、`TEXT`（字符串）、`REAL`（浮点数）、`BLOB`（二进制数据）、`NULL`（空值）。

## 五、常用工具（可选）

若想可视化查看 `test.db` 中的数据，推荐工具：

- Windows：SQLite Expert、Navicat；
- Mac：DB Browser for SQLite（免费开源）；
- 在线工具：SQLite Online（无需安装，直接上传 `.db` 文件查看）。

按以上步骤操作，即可完成 Python 对 SQLite 的全流程操作，适合小型项目、本地存储、原型开发等场景！

编辑分享

如何在 Python 中使用 SQLite 数据库进行数据查询？

如何在 Python 中使用 SQLite 数据库进行数据更新？

如何在 Python 中使用 SQLite 数据库进行数据删除？