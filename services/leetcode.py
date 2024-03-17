from utils.graphql import send_leetcode_graphql_request

# 获取每日一题的基本信息
def get_daily_question():
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
    data = send_leetcode_graphql_request(query, variables)
    daily_question = data["data"]["calendarTaskSchedule"]["dailyQuestions"][0]
    return daily_question

# 获取题目详细信息
def get_question_details(slug):
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
    data = send_leetcode_graphql_request(query, variables)
    return data

# 获取题目内容和难度信息
def get_question_content(slug):
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
    data = send_leetcode_graphql_request(query, variables)
    return data["data"]["question"]

# 获取完整的每日一题数据
def get_daily_question_data():
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
