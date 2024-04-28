import ast
import os
import sqlite3
import sys
from datetime import datetime, timedelta
from push import push_message
import requests
import xml.etree.ElementTree as ET
import re
import traceback


rss_url = "https://rss.nodeseek.com/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# 数据库文件路径
database_file = "sent_guids.db"


def create_database():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS sent_guids (
                        guid TEXT PRIMARY KEY,
                        timestamp TEXT)''')
    conn.commit()
    conn.close()


def check_sent_guid(guid):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sent_guids WHERE guid=?", (guid,))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def save_sent_guid(guid):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sent_guids (guid, timestamp) VALUES (?, ?)", (guid, timestamp))
    conn.commit()
    conn.close()


def extract_telegram_username(description):
    username_pattern = r"@([a-zA-Z0-9_]{5,})"
    match = re.search(username_pattern, description)
    if match:
        return match.group(1)
    else:
        return None


def clean_old_guids():
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sent_guids WHERE datetime(timestamp) < datetime('now', '-1 day')")
    conn.commit()
    conn.close()


def fetch_and_send_data():
    t_kwd = get_keywords("t_keywords")
    d_kwd = get_keywords("d_keywords")
    b_kwd = get_keywords("b_keywords")
    if not t_kwd or not d_kwd:
        return
    try:
        response = requests.get(rss_url, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            for item in root.findall(".//item"):
                title = item.findtext("title")
                description = item.findtext("description")
                link = item.findtext("link")
                guid = item.findtext("guid")
                category = item.findtext("category")
                pub_date = item.findtext("pubDate")
                category = str(category)

                pub_date = datetime.strptime(pub_date, "%a, %d %b %Y %H:%M:%S GMT")
                pub_date_beijing = pub_date + timedelta(hours=8)
                if 0 <= pub_date_beijing.hour < 7:
                    continue

                if not b_kwd:
                    if any(keyword in title or keyword in description for keyword in b_kwd):
                        continue

                send_flag = False
                if any(keyword in title or keyword in category.strip().lower() for keyword in t_kwd):
                    send_flag = True
                elif description is not None and description.strip() != "":
                    if any(keyword in description for keyword in d_kwd):
                        send_flag = True
                if send_flag:
                    if not check_sent_guid(guid):
                        print(title, description, link, guid)
                        message = f"{description}\n----\n{link}"
                        username = extract_telegram_username(str(description))
                        if username:
                            message += f"\nTG: https://t.me/{username}"
                        push_message(title, message)
                        save_sent_guid(guid)
    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        push_message("NodeSeek Error", str(e))
    finally:
        clean_old_guids()


def get_keywords(variable_name):
    keywords_str = os.getenv(variable_name)

    if keywords_str:
        # 尝试将字符串转换为列表
        try:
            keywords = ast.literal_eval(keywords_str)
        except ValueError as e:
            print(f"环境变量 {variable_name} 为空，请检查格式是否正确。正确示例 ['出', '收']", e)
            keywords = []
    else:
        print(f"环境变量 {variable_name} 不存在.")
        keywords = []
    return keywords


if __name__ == "__main__":
    create_database()
    fetch_and_send_data()
