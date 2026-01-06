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