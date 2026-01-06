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