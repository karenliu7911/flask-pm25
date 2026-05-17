import pymysql
import pandas as pd
import requests, io
from datetime import datetime
import urllib3
import os
from dotenv import load_dotenv

load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_data_by_county(county):
    conn, cursor = open_db()
    result = {"success": True, "message": None, "columns": None, "rows": None}

    if not conn:
        result["success"] = False
        result["message"] = "資料庫開啟失敗"  # 與open_db()有關
        return result

    sql = """select * from data where county=%s
    and datacreationdate=(select max(datacreationdate) from data);   
    """
    try:
        cursor.execute(sql, (county,))

        # 取得資料欄位名稱
        rows = cursor.fetchall()
        result["success"] = True
        result["rows"] = rows
        return result

    except Exception as e:
        result["success"] = False
        result["message"] = f"資料庫查詢失敗:{e}"  # 與SQL語法有關
        return result
    finally:
        conn.close()


# 取得不重覆縣市
def get_counties():
    conn, cursor = open_db()
    result = {"success": True, "message": None, "rows": None}

    if not conn:
        result["success"] = False
        result["message"] = "資料庫開啟失敗"  # 與open_db()有關
        return result

    sql = "select DISTINCT county from data ORDER by county desc;"

    try:
        cursor.execute(sql)

        # 取得資料欄位名稱
        rows = cursor.fetchall()
        result["success"] = True
        result["rows"] = rows
        return result

    except Exception as e:
        result["success"] = False
        result["message"] = f"資料庫查詢失敗:{e}"  # 與SQL語法有關
        return result
    finally:
        conn.close()


def get_latest_data():
    conn, cursor = open_db()
    result = {"success": True, "message": None, "columns": None, "rows": None}

    if not conn:
        result["success"] = False
        result["message"] = "資料庫開啟失敗"  # 與open_db()有關
        return result

    # SQL語法
    sql = """
    select * from data where datacreationdate=
    (select max(datacreationdate) from data);
    """

    # sql = 'select max(datacreationdate) from data;'

    try:
        cursor.execute(sql)

        # 取得資料欄位名稱
        # print(cursor.description)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        result["success"] = True
        result["columns"] = columns
        result["rows"] = rows
        return result

    except Exception as e:
        result["success"] = False
        result["message"] = f"資料庫查詢失敗:{e}"  # 與SQL語法有關
        return result
    finally:
        conn.close()


def open_db():
    try:

        conn = pymysql.connect(
            host=os.getenv("HOST"),
            port=int(os.getenv("PORT")),
            user=os.getenv("USER"),
            password=os.getenv("PASSWORD"),
            database=os.getenv("NAME"),
            ssl={"ca": None},
        )

        cursor = conn.cursor()

        return conn, cursor
    except Exception as e:
        print(e)

    return None, None


if __name__ == "__main__":
    # print(open_db())  測試是否有連接資料庫
    print(get_data_by_county("新北市"))
