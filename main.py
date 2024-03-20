# main.py
from fastapi import FastAPI
import json
from bson import ObjectId
from typing import Any
from apis.daily_question import router as daily_question_router
from repositories.mongodb_repository import MongoDBRepository
from graphql_client import GraphQLClient
from services.leetcode_service import LeetCodeService
from config import config
import logging
# 自定义JSON编码器
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, ObjectId):
            return str(o)
        elif isinstance(o, datetime):
            return o.isoformat()
        elif hasattr(o, 'to_dict'):
            return o.to_dict()
        else:
            return json.JSONEncoder.default(self, o)


app = FastAPI(json_encoder=CustomJSONEncoder)
app.include_router(daily_question_router)

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# 初始化依赖
mongo_repo = MongoDBRepository()
graphql_client = GraphQLClient(config.GRAPHQL_URL)
leetcode_service = LeetCodeService(mongo_repo, graphql_client)

# 将服务实例注入到相关模块中
daily_question_router.leetcode_service = leetcode_service

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
