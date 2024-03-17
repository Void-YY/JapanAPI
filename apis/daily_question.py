from fastapi import APIRouter
from services.leetcode import get_daily_question_data

# 创建路由对象
router = APIRouter()

# 定义API路由,返回每日一题数据
@router.get("/daily-question")
def get_daily_question_api():
    return get_daily_question_data()
