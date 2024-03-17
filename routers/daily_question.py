# routers/daily_question.py
from fastapi import APIRouter
import requests

# 创建路由对象
router = APIRouter()

# 获取每日一题
def get_daily_question():
    """
    从LeetCode获取每日一题的基本信息

    Returns:
        dict: 包含每日一题的id、名称、slug、链接和是否为加密题目的字典
    """
    query = """
    query CalendarTaskSchedule($days: Int!) {
        calendarTaskSchedule(days: $days) {
            dailyQuestions {
                id
                name
                slug
                link
                premiumOnly
            }
        }
    }
    """
    variables = {"days": 0}
    url = "https://leetcode.cn/graphql/"
    json = {
        "query": query,
        "variables": variables,
        "operationName": "CalendarTaskSchedule"
    }
    response = requests.post(url, json=json)
    data = response.json()
    daily_question = data["data"]["calendarTaskSchedule"]["dailyQuestions"][0]
    return daily_question

# 获取题目详细信息
def get_question_details(slug):
    """
    根据题目的slug从LeetCode获取该题目的详细信息

    Args:
        slug (str): 题目的slug

    Returns:
        dict: 包含题目详细信息的字典
    """
    query = """
    query usernameConfigs($slugs: [String!]!) {
        userProfileUserPendants(userSlugs: $slugs) {
            id
            config {
                iconWearing
            }
            name
            category
            month
        }
        userProfileUserColors(userSlugs: $slugs)
        reputationUserReputations(userSlugs: $slugs) {
            level
            reputation
            user {
                userSlug
            }
        }
    }
    """
    variables = {"slugs": [slug]}
    url = "https://leetcode.cn/graphql/"
    json = {
        "query": query,
        "variables": variables,
        "operationName": "usernameConfigs"
    }
    response = requests.post(url, json=json)
    data = response.json()
    return data

# 获取题目详细内容和难度等信息
def get_question_content(slug):
    """
    根据题目的slug从LeetCode获取该题目的详细内容和难度等信息

    Args:
        slug (str): 题目的slug

    Returns:
        dict: 包含题目详细内容和难度等信息的字典
    """
    query = """
    query questionTranslations($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            translatedTitle
            translatedContent
            difficulty
        }
    }
    """
    variables = {"titleSlug": slug}
    url = "https://leetcode.cn/graphql/"
    json = {
        "query": query,
        "variables": variables,
        "operationName": "questionTranslations"
    }
    response = requests.post(url, json=json)
    data = response.json()
    return data["data"]["question"]

# 定义路由
@router.get("/daily-question")
def get_daily_question_api():
    """
    获取每日一题的API端点

    Returns:
        dict: 包含每日一题的基本信息、详细信息和详细内容的字典
    """
    daily_question = get_daily_question()
    question_details = get_question_details(daily_question["slug"])
    question_content = get_question_content(daily_question["slug"])
    return {
        "question_id": daily_question["id"],
        "question_name": daily_question["name"],
        "question_slug": daily_question["slug"],
        "question_link": daily_question["link"],
        "question_details": question_details,
        "question_content": question_content
    }
