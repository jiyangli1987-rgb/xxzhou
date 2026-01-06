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