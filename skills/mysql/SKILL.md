---
name: mysql-processing
description: 连接 MySQL 数据库，对表中的数据进行查询、修改、删除等操作。
---
# MySQL 数据库操作

连接 MySQL 数据库，对表中的数据进行查询、修改、删除等操作。

## 功能列表

1. **连接数据库** - 建立与 MySQL 数据库的连接
2. **查询所有表** - 列出数据库中的所有表
3. **操作表结构** - 添加或删除字段
4. **操作表数据** - 新增、查询、修改、删除数据
5. **执行自定义 SQL** - 执行任意 SQL 语句

## 前置要求

确保已安装 Python 依赖：

```bash
pip install pymysql
```

## 使用说明

### 1. 查询数据库中的所有表

```bash
python scripts/mysql_ops.py list_tables '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database"}'
```

### 2. 添加字段

```bash
python scripts/mysql_ops.py add_column '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "column_name": "email", "column_type": "VARCHAR(255)"}'
```

### 3. 删除字段

```bash
python scripts/mysql_ops.py drop_column '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "column_name": "email"}'
```

### 4. 查询数据

```bash
python scripts/mysql_ops.py query_data '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "where": "id > 10", "limit": 1000}'
```

### 5. 插入数据

```bash
python scripts/mysql_ops.py insert_data '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "data": {"name": "张三", "age": 25}}'
```

### 6. 更新数据

```bash
python scripts/mysql_ops.py update_data '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "data": {"name": "李四"}, "where": "id = 1"}'
```

### 7. 删除数据

```bash
python scripts/mysql_ops.py delete_data '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "table": "users", "where": "id = 1"}'
```

### 8. 执行自定义 SQL

```bash
python scripts/mysql_ops.py execute_sql '{"host": "localhost", "port": 3306, "user": "root", "password": "your_password", "database": "your_database", "sql": "SELECT * FROM users WHERE age > 18"}'
```

## 参数说明

### 通用参数

- `host`: 数据库主机地址（默认 localhost）
- `port`: 数据库端口（默认 3306）
- `user`: 数据库用户名
- `password`: 数据库密码
- `database`: 数据库名称

### 操作特定参数

- `table`: 表名
- `column_name`: 字段名
- `column_type`: 字段类型（如 VARCHAR(255), INT, TEXT 等）
- `data`: 数据对象（JSON 格式）
- `where`: WHERE 条件子句
- `limit`: 查询结果限制数量（默认 100）
- `sql`: 自定义 SQL 语句

## 使用示例

当用户说"查询 users 表中的所有数据"时，你应该：

```bash
python scripts/mysql_ops.py query_data '{"host": "localhost", "port": 3306, "user": "root", "password": "password", "database": "mydb", "table": "users"}'
```

当用户说"给 products 表添加一个 price 字段，类型为 DECIMAL(10,2)"时，你应该：

```bash
python scripts/mysql_ops.py add_column '{"host": "localhost", "port": 3306, "user": "root", "password": "password", "database": "mydb", "table": "products", "column_name": "price", "column_type": "DECIMAL(10,2)"}'
```

## 注意事项

1. 所有操作都需要提供数据库连接信息
2. 删除字段和删除数据操作不可逆，请谨慎使用
3. 执行自定义 SQL 时，请确保 SQL 语句的安全性
4. 建议在生产环境使用只读账户进行查询操作
5. 密码等敏感信息请妥善保管，不要硬编码在代码中

## 返回格式

所有操作返回 JSON 格式的结果：

- 成功时：`{"success": true, "message": "...", "data": [...]}`
- 失败时：`{"error": "错误信息"}`
