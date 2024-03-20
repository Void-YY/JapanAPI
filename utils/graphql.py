# utils\graphql.py
import requests

def send_leetcode_graphql_request(query, variables):
    url = "https://leetcode.cn/graphql/"
    json = {
        "query": query,
        "variables": variables,
        "operationName": None  # 根据需要设置operationName
    }
    response = requests.post(url, json=json)
    return response.json()
