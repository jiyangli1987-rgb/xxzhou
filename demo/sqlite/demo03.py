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