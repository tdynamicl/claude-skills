#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MySQL数据库操作工具"""

import sys
import json
import pymysql
from pymysql.cursors import DictCursor

def connect_db(host, port, user, password, database=None):
    """连接数据库"""
    try:
        conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            cursorclass=DictCursor
        )
        return conn, None
    except Exception as e:
        return None, str(e)

def list_tables(host, port, user, password, database):
    """列出数据库中的所有表"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]
        return {"tables": tables}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def add_column(host, port, user, password, database, table, column_name, column_type):
    """添加字段"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            sql = f"ALTER TABLE `{table}` ADD COLUMN `{column_name}` {column_type}"
            cursor.execute(sql)
        conn.commit()
        return {"success": True, "message": f"字段 {column_name} 已添加"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def drop_column(host, port, user, password, database, table, column_name):
    """删除字段"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            sql = f"ALTER TABLE `{table}` DROP COLUMN `{column_name}`"
            cursor.execute(sql)
        conn.commit()
        return {"success": True, "message": f"字段 {column_name} 已删除"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def query_data(host, port, user, password, database, table, where=None, limit=100):
    """查询数据"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            sql = f"SELECT * FROM `{table}`"
            if where:
                sql += f" WHERE {where}"
            sql += f" LIMIT {limit}"
            cursor.execute(sql)
            rows = cursor.fetchall()
        return {"data": rows, "count": len(rows)}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def insert_data(host, port, user, password, database, table, data):
    """插入数据"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            columns = ', '.join([f"`{k}`" for k in data.keys()])
            placeholders = ', '.join(['%s'] * len(data))
            sql = f"INSERT INTO `{table}` ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(data.values()))
        conn.commit()
        return {"success": True, "message": "数据已插入", "id": cursor.lastrowid}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def update_data(host, port, user, password, database, table, data, where):
    """更新数据"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            set_clause = ', '.join([f"`{k}`=%s" for k in data.keys()])
            sql = f"UPDATE `{table}` SET {set_clause} WHERE {where}"
            cursor.execute(sql, list(data.values()))
        conn.commit()
        return {"success": True, "message": f"已更新 {cursor.rowcount} 行"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def delete_data(host, port, user, password, database, table, where):
    """删除数据"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            sql = f"DELETE FROM `{table}` WHERE {where}"
            cursor.execute(sql)
        conn.commit()
        return {"success": True, "message": f"已删除 {cursor.rowcount} 行"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def execute_sql(host, port, user, password, database, sql):
    """执行自定义SQL"""
    conn, err = connect_db(host, port, user, password, database)
    if err:
        return {"error": err}

    try:
        with conn.cursor() as cursor:
            cursor.execute(sql)
            if sql.strip().upper().startswith('SELECT'):
                rows = cursor.fetchall()
                return {"data": rows, "count": len(rows)}
            else:
                conn.commit()
                return {"success": True, "affected_rows": cursor.rowcount}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "缺少操作参数"}))
        sys.exit(1)

    operation = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}

    operations = {
        "list_tables": list_tables,
        "add_column": add_column,
        "drop_column": drop_column,
        "query_data": query_data,
        "insert_data": insert_data,
        "update_data": update_data,
        "delete_data": delete_data,
        "execute_sql": execute_sql
    }

    if operation not in operations:
        print(json.dumps({"error": f"未知操作: {operation}"}))
        sys.exit(1)

    result = operations[operation](**params)
    print(json.dumps(result, ensure_ascii=False, indent=2))
