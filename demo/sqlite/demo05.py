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