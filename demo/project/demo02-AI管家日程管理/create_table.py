import sqlite3
from datetime import datetime
from typing import Optional,Literal
from pydantic import BaseModel,Field

class DataModel(BaseModel):
    # 任务标题：必填 + 长度约束（避免空标题/超长标题）
    title: str = Field(
        ...,  # 表示必填（你的写法默认允许 None，建议显式必填）
        min_length=1,
        max_length=100,
        description="任务标题"
    )
    
    # 创建时间：支持字符串（如 ISO 格式）自动转 datetime，也可直接传 datetime
    created_at: datetime = Field(
        description="创建时间（支持格式：YYYY-MM-DD HH:MM:SS 或 ISO 格式，如 2025-12-18T14:30:00）"
    )
    
    # 截止时间：同上 + 必须晚于创建时间
    end_time: datetime = Field(
        description="截止时间（格式同创建时间，需晚于创建时间）"
    )
    
    # 权重：用 Literal 限定可选值（统一标准），比 str 更规范
    weight: Literal["高", "普通"] = Field(
        default="默认",  # 可选：设置默认值，无需手动传入
        description="权重（可选值：高/中/低/默认）"
    )






def create_task_table(db_path: str = "task_db.sqlite3") -> None:
    """
    创建任务表（对应 DataModel 数据结构）
    :param db_path: SQLite 数据库文件路径
    """
    # 连接数据库（不存在则自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL 创建表语句
    # 字段映射说明：
    # - title: 字符串（VARCHAR）+ 非空 + 长度1-100
    # - created_at: 时间戳（DATETIME）+ 非空（支持 ISO 格式字符串自动转换，在插入时处理）
    # - end_time: 时间戳（DATETIME）+ 非空 + 检查约束（必须晚于 created_at）
    # - weight: 字符串（VARCHAR）+ 枚举约束（高/普通/默认）+ 默认值"默认"
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        -- 自增主键（实际业务中建议添加，用于唯一标识任务）
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        
        -- 任务标题：必填 + 长度1-100
        title VARCHAR(100) NOT NULL CHECK (LENGTH(title) >= 1),
        
        -- 创建时间：非空（SQLite 支持 ISO 格式字符串自动解析为 datetime）
        created_at DATETIME NOT NULL,
        
        -- 截止时间：非空 + 必须晚于创建时间
        end_time DATETIME NOT NULL CHECK (end_time > created_at),
        
        -- 权重：枚举约束 + 默认值
        weight VARCHAR(10) NOT NULL DEFAULT '默认' 
            CHECK (weight IN ('高', '普通', '默认')),
        
        -- 字段注释（SQLite 3.24.0+ 支持，低版本可忽略 COMMENT 部分）
        COMMENT '任务表（对应 DataModel 数据结构）'
    );

    -- 可选：为常用查询字段创建索引（提升查询性能）
    CREATE INDEX IF NOT EXISTS idx_tasks_created_at ON tasks(created_at);
    CREATE INDEX IF NOT EXISTS idx_tasks_end_time ON tasks(end_time);
    CREATE INDEX IF NOT EXISTS idx_tasks_weight ON tasks(weight);
    """

    try:
        # 执行 SQL 语句（支持多行 SQL）
        cursor.executescript(create_table_sql)
        conn.commit()
        print(f"✅ 任务表创建成功（数据库文件：{db_path}）")
    except Exception as e:
        conn.rollback()
        print(f"❌ 表创建失败：{str(e)}")
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

def insert_sample_data(task_data: DataModel,db_path: str = "task_db.sqlite3",) -> Optional[int]:
    """
    插入示例数据（演示数据类型兼容性）
    :param db_path: 数据库路径
    :param task_data: 任务数据（符合 DataModel 结构）
    :return: 插入数据的主键 ID
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    insert_sql = """
    INSERT INTO tasks (title, created_at, end_time, weight)
    VALUES (?, ?, ?, ?)
    """

    try:
        # 处理 datetime 类型（自动转换为 ISO 格式字符串，SQLite 可识别）
        params = (
            task_data["title"],
            task_data["created_at"].isoformat() if isinstance(task_data["created_at"], datetime) else task_data["created_at"],
            task_data["end_time"].isoformat() if isinstance(task_data["end_time"], datetime) else task_data["end_time"],
            task_data.get("weight", "默认")  # 使用默认值
        )

        cursor.execute(insert_sql, params)
        conn.commit()
        print(f"✅ 数据插入成功，主键 ID：{cursor.lastrowid}")
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        print(f"❌ 数据插入失败：{str(e)}")
        return None
    finally:
        cursor.close()
        conn.close()

# if __name__ == "__main__":
#     # 1. 创建表
#     create_task_table()

#     # 2. 插入示例数据（验证约束和格式兼容性）
#     sample_task = {
#         "title": "完成 SQLite 表设计",
#         "created_at": datetime.now(),  # 直接传 datetime 对象
#         "end_time": datetime(2025, 12, 20, 18, 0),  # 截止时间晚于创建时间
#         "weight": "高"
#     }

#     insert_sample_data(task_data=sample_task)

#     # 插入测试：故意违反约束（会报错，验证约束生效）
#     invalid_task = {
#         "title": "",  # 违反长度约束
#         "created_at": "2025-12-18T14:30:00",  # 传 ISO 格式字符串
#         "end_time": "2025-12-17T14:30:00",  # 截止时间早于创建时间（违反 CHECK 约束）
#         "weight": "超高"  # 违反权重枚举约束
#     }
#     insert_sample_data(task_data=invalid_task)