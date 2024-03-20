# repositories\mongodb_repository.py
import logging
from pymongo import MongoClient
from config import config

logger = logging.getLogger(__name__)

class MongoDBRepository:
    def __init__(self):
        self.client = MongoClient(config.MONGO_URI)
        self.db = self.client[config.MONGO_DB]
        self.collection = self.db[config.MONGO_COLLECTION]

    def save_data(self, data):
        try:
            self.collection.delete_one({"question_slug": data["question_slug"]})
            self.collection.insert_one(data)
            logger.info(f"Successfully saved daily question data to MongoDB: {data['question_slug']}")
        except Exception as e:
            logger.error(f"Error occurred while saving daily question data to MongoDB: {e}")
            raise Exception("Failed to save daily question data to MongoDB")
