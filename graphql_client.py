# graphql_client.py
import requests
import logging

logger = logging.getLogger(__name__)

class GraphQLClient:
    def __init__(self, url):
        self.url = url

    def send_request(self, query, variables):
        try:
            json = {
                "query": query,
                "variables": variables
            }
            response = requests.post(self.url, json=json)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error occurred while sending GraphQL request: {e}")
            raise Exception("Failed to send GraphQL request")
