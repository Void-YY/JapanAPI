# services\leetcode_service.py
import logging
import re
from repositories.mongodb_repository import MongoDBRepository
from graphql_client import GraphQLClient
from exceptions import GraphQLRequestException, DataProcessingException

logger = logging.getLogger(__name__)

class LeetCodeService:
    def __init__(self, mongo_repo: MongoDBRepository, graphql_client: GraphQLClient):
        self.mongo_repo = mongo_repo
        self.graphql_client = graphql_client

    def get_daily_question_data(self):
        try:
            daily_question = self._get_daily_question()
            question_details = self._get_question_details(daily_question["slug"])
            question_content = self._get_question_content(daily_question["slug"])
        except Exception as e:
            logger.error(f"Error occurred while getting daily question data: {e}")
            raise GraphQLRequestException("Failed to get daily question data")

        try:
            processed_data = self._process_data(daily_question, question_details, question_content)
            self.mongo_repo.save_data(processed_data)
        except Exception as e:
            logger.error(f"Error occurred while processing or saving daily question data: {e}")
            raise DataProcessingException("Failed to process or save daily question data")

        return processed_data

    def _get_daily_question(self):
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
        data = self.graphql_client.send_request(query, variables)
        daily_question = data["data"]["calendarTaskSchedule"]["dailyQuestions"][0]
        return daily_question

    def _get_question_details(self, slug):
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
        data = self.graphql_client.send_request(query, variables)
        return data

    def _get_question_content(self, slug):
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
        data = self.graphql_client.send_request(query, variables)
        return data["data"]["question"]

    def _process_data(self, daily_question, question_details, question_content):
        # 提取图片链接
        img_pattern = re.compile(r'<img.*?src=["\'](.*?)["\']', re.IGNORECASE)
        image_list = img_pattern.findall(question_content["translatedContent"])

        # 移除HTML标签
        html_pattern = re.compile(r'<.*?>')
        clean_content = re.sub(html_pattern, '', question_content["translatedContent"])

        # 构造要保存到MongoDB的数据
        mongo_data = {
            "question_id": daily_question["id"],
            "question_name": daily_question["name"],
            "question_slug": daily_question["slug"],
            "question_link": daily_question["link"],
            "translated_title": question_content["translatedTitle"],
            "translated_content": clean_content,
            "difficulty": question_content["difficulty"],
            "image_list": image_list
        }

        return mongo_data
