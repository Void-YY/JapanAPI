# tasks/daily_question.py
import schedule
import time
import re
from datetime import datetime, timedelta, tzinfo
from services.leetcode_service import get_daily_question_data
from pymongo import MongoClient
import threading
from . import config

# MongoDB连接配置
client = MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB]
collection = db[config.MONGO_COLLECTION]

# 定义东九区时区
class EastNineZone(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

# 整理并保存数据到MongoDB
def save_data_to_mongodb(data):
    # 提取图片链接
    img_pattern = re.compile(r'<img.*?src=["\'](.*?)["\']', re.IGNORECASE)
    image_list = img_pattern.findall(data["question_content"]["translatedContent"])

    # 移除HTML标签
    html_pattern = re.compile(r'<.*?>')
    clean_content = re.sub(html_pattern, '', data["question_content"]["translatedContent"])

    # 构造要保存到MongoDB的数据
    mongo_data = {
        "question_id": data["question_id"],
        "question_name": data["question_name"],
        "question_slug": data["question_slug"],
        "question_link": data["question_link"],
        "translated_title": data["question_content"]["translatedTitle"],
        "translated_content": clean_content,
        "difficulty": data["question_content"]["difficulty"],
        "image_list": image_list
    }

    # 保存到MongoDB
    collection.delete_one({"question_slug": data["question_slug"]})
    collection.insert_one(mongo_data)
    print(f"更新LeetCode题目成功: {datetime.now(EastNineZone())}")

# 定时任务,获取每日一题数据并存储到MongoDB
def daily_question_task():
    data = get_daily_question_data()
    save_data_to_mongodb(data)

# 设置定时任务,每天东九区早晨8点半执行
def start_daily_question_task():
    schedule.every().day.at("08:30").do(daily_question_task)

    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)

    # 启动后台线程运行定时任务
    threading.Thread(target=run_scheduler).start()
