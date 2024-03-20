class LeetCodeException(Exception):
    """自定义LeetCode异常类"""
    pass

class GraphQLRequestException(LeetCodeException):
    """GraphQL请求异常"""
    pass

class DataProcessingException(LeetCodeException):
    """数据处理异常"""
    pass
