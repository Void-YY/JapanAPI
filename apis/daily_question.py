# apis/daily_question.py
from fastapi import APIRouter
from services.leetcode_service import LeetCodeService
from repositories.mongodb_repository import MongoDBRepository
from graphql_client import GraphQLClient
from config import config
from exceptions import LeetCodeException

router = APIRouter()

@router.get("/daily-question")
async def get_daily_question_api():
    try:
        mongo_repo = MongoDBRepository()
        graphql_client = GraphQLClient(config.GRAPHQL_URL)
        leetcode_service = LeetCodeService(mongo_repo, graphql_client)
        data = leetcode_service.get_daily_question_data()
        # 删除_id字段
        if '_id' in data:
            del data['_id']

        return data
    except LeetCodeException as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": "An unexpected error occurred."}
