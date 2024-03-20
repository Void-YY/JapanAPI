# config.py
import os
from dotenv import load_dotenv
# 加载 .env 文件中的环境变量
load_dotenv()
class Config:
    GRAPHQL_URL = os.getenv('GRAPHQL_URL')
    MONGO_URI = os.getenv('MONGO_URI')
    MONGO_DB = os.getenv('MONGO_DB')
    MONGO_COLLECTION = os.getenv('MONGO_COLLECTION')

config = Config()
